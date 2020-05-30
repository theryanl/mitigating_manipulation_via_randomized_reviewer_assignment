#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cmath>
#include <algorithm>

using namespace std;

const int N = 100005, M = 50000005, one = 10000000, dig = 7, debug = 0;

int p, r, n, m, h[N], u[M], v[M], l[M], s[N], se[M], tot = 1;
int hi[N], vi[M], li[M], ri[N], si[M], ti;
int st[M], top, btm;
int f[M], c[N], ci[M], fw, bw;

int fl(int x)
{
    return floor(double(x) / one) * one;
}

int ce(int x)
{
    return ceil(double(x) / one) * one;
}

bool in(int x)
{
    return x == fl(x) || x == ce(x);
}

void ae(int x, int y, int z)
{
    ++m;
    u[++tot] = x;
    v[tot] = y;
    f[tot] = z;
    l[tot] = h[x];
    h[x] = tot;
}

int fi(int p, int i)
{
    for(int j = hi[p]; j; j = li[j])
        if(vi[j] == i) return j;
    return 0;
}

void ai(int p, int i, int w)
{
    int j = fi(p, i);
    if(j)
        ci[j] += w;
    else
    {
        vi[++ti] = i;
        li[ti] = hi[p];
        ci[ti] = w;
        hi[p] = ti;
    }
}

void re(int x)
{
    --m;
    int t = u[x];
    if(x == h[t])
    {
        h[t] = l[x];
        return;
    }
    int i = h[t];
    while(l[i] != x)
        i = l[i];
    l[i] = l[x];
}

int tr(int x, int i)
{
    if(!hi[x])
    {
        for(int j = h[x]; j; j = l[j])
            if(!se[j]) return j;
    }
    else if(!i)
    {
        for(int j = hi[x]; j; j = li[j])
            if(!in(ci[j]))
            {
                int t = tr(x, vi[j]);
                if(t) return t;
            }
    }
    else
        for(int j = h[x]; j; j = l[j])
            if(ri[v[j]] == i && !se[j]) return j;
    return 0;
}

void cnr(int x)
{
    if(f[x] == 0 || f[x] == one)
    {
        re(x);
        re(x ^ 1);
    }
}

void upd(int x, int y)
{
    f[x] -= y;
    f[x ^ 1] += y;
    c[u[x]] -= y;
    c[v[x]] += y;

    if(hi[v[x]])
        ai(v[x], ri[u[x]], -y);
    else
        ai(u[x], ri[v[x]], y);

    cnr(x);
}

int go(int x, int y, int p) // x: current vertex, y: previous edge, p: whether finding a path
{
    if(debug) printf("%d %d %d %d\n", x, y, p, top);
    if(y) st[++top] = y;
    int ret = 0, t = 0, yi = 0, zi = 0;

    if(!hi[x]) // x is a reviewer
    {
        if(debug) printf("c: %d\n", c[x]);
        if(s[x]) // found a cycle
        {
            fw = bw = one;
            btm = 0;

            for(int i = 1; i <= top; i++)
                if(u[st[i]] == x)
                {
                    btm = i;
                    break;
                }

            if(debug) printf("r cycle: %d\n", btm);

            return 1;
        }

        if(y && p && (!in(c[x]))) // found a path
        {
            fw = ce(c[x]) - c[x];
            bw = c[x] - fl(c[x]);
            btm = 1;
            if(debug) printf("r path: %d\n", btm);
            return 1;
        }

        s[x] = 1;
        t = tr(x, 0);

        if(!t)
        {
            if(debug && y) printf("r dead end\n");
            fw = bw = 0;
            return 0;
        }
        if(debug) printf("f[t]: %d\n", f[t]);
        se[t] = se[t ^ 1] = 1;
        ret = go(v[t], t, p);
        se[t] = se[t ^ 1] = 0;
        fw = min(fw, f[t]);
        bw = min(bw, f[t ^ 1]);
    }
    else // x is a paper
    {
        yi = fi(x, ri[u[y]]); // set yi to institution of incoming edge

        if(debug) printf("c: %d, ci: %d\n", c[x], ci[yi]);
        
        if(si[yi]) // found an ``even'' cycle (never happens when y = yi = 0)
        {
            fw = bw = one;
            btm = 0;

            for(int i = 1; i <= top; i++)
                if(u[st[i]] == x && ri[v[st[i]]] == vi[yi]) // find first edge in stack (1) leaving x and (2) going to institution of incoming edge -- cycle starts there
                {
                    btm = i;
                    break;
                }

            if(debug) printf("p even cycle: %d\n", btm);
            
            return 1;
        }

        if(s[x] && !in(ci[yi])) // found an ``odd'' cycle
        {
            fw = ci[yi] - fl(ci[yi]);
            bw = ce(ci[yi]) - ci[yi];
            btm = 0;

            int wi = 0;

            for(int i = 1; i <= top; i++)
                if(u[st[i]] == x)
                {
                    wi = fi(x, ri[v[st[i]]]);
                    if(!in(ci[wi]))
                    {
                        btm = i;
                        break;
                    }
                }

            fw = min(fw, ce(ci[wi]) - ci[wi]);
            bw = min(bw, ci[wi] - fl(ci[wi]));

            if(debug) printf("p odd cycle: %d\n", btm);

            return 1;
        }

        if(y && p && (!in(c[x])) && (!in(ci[yi]))) // found a path
        {
            fw = ce(c[x]) - c[x];
            bw = c[x] - fl(c[x]);
            fw = min(fw, ci[yi] - fl(ci[yi]));
            bw = min(bw, ce(ci[yi]) - ci[yi]);
            btm = 1;
            if(debug) printf("p path: %d\n", btm);
            return 1;
        }
    
        if(in(ci[yi])) // integral institution load -- leave through the same institution (equivalent to the other case when y = yi = 0)
            t = tr(x, vi[yi]);
        else // leave through any fractional institution
            t = tr(x, 0);

        if(!t)
        {
            fw = bw = 0;
            if(debug && y) printf("p dead end\n");
            return 0;
        }

        if(debug) printf("f[t]: %d\n", f[t]);

        zi = fi(x, ri[v[t]]); // set zi to instituion of outgoing edge
        si[zi] = 1;
        se[t] = se[t ^ 1] = 1;
        if(!in(ci[zi])) s[x] = 1;

        ret = go(v[t], t, p);

        si[zi] = 0;
        se[t] = se[t ^ 1] = 0;

        fw = min(fw, f[t]);
        bw = min(bw, f[t ^ 1]);
        
        
    }

    if(t == st[btm] && fw + bw != 0)
    {
        if((!y) && p)
        {
            fw = min(fw, c[x] - fl(c[x]));
            bw = min(bw, ce(c[x]) - c[x]);
            if(hi[x])
            {
                int yi = fi(x, ri[v[t]]);
                fw = min(fw, ce(ci[yi]) - ci[yi]);
                bw = min(bw, ci[yi] - fl(ci[yi]));
            }
        }
        if(debug) printf("clearing a path/cycle: %d %d\n", fw, bw);
        int r, d;
        if(double(rand()) / RAND_MAX < double(bw) / (fw + bw))
        {
            d = 1;
            r = fw;
        }
        else
        {
            d = -1;
            r = bw;
        }

        for(int i = btm; i <= top; i++) upd(st[i], r * d);
        fw = bw = 0;
    }

    if(hi[x] && yi != zi) // must update after clearing cycle/path
    {
        fw = min(fw, ce(ci[zi]) - ci[zi]);
        bw = min(bw, ci[zi] - fl(ci[zi]));

        fw = min(fw, ci[yi] - fl(ci[yi]));
        bw = min(bw, ce(ci[yi]) - ci[yi]);
    }

    return ret;
}

int main()
{
    srand(time(0));
    rand();

    scanf("%d%d", &r, &p);
    n = p + r;

    int x, y, z;
    char sz[100];

    for(int i = 1; i <= r; i++) scanf("%d", &ri[i]);
    // for(int i = 1; i <=r; i++) ri[i] = rand() % 2 + 1;

    for(int i = 0; i < p * r; i++)
    {
        scanf("%d%d%s", &x, &y, sz);
        ++x;
        ++y;

        if(strlen(sz) <= 2) z = one * (sz[0] == '1');
        else
        {
            sz[dig + 2] = 0;
            sscanf(sz + 2, "%d", &z);
            for(int j = strlen(sz + 2); j < dig; j++) z *= 10;
        }

        c[x] += z;
        c[y] -= z;
        if(z != 0)
        {
            ae(x, y, z);
            ae(y, x, one - z);

            ai(y, ri[x], z);
        }
    }

    while(m)
    {
        if(debug) printf("%d\n", m);
        memset(s, 0, sizeof(s));
        for(int i = 1; i <= n; i++)
            if(!in(c[i]))
            {
                top = 0;
                if(go(i, 0, 1)) break;
            }

        memset(s, 0, sizeof(s));
        for(int i = 1; i <= n; i++)
        {
            top = 0;
            if(go(i, 0, 0)) break;
        }
    }

    for(int i = 2; i <= tot; i++)
        if(u[i] < v[i] && f[i] == one)
            printf("%d %d\n", u[i] - 1, v[i] - 1);

    return 0;
}
