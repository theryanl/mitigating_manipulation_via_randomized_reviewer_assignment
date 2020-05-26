#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cmath>
#include <algorithm>

using namespace std;

const int N = 100005, M = 100000005, one = 10000000, dig = 7;

int p, r, n, m, h[N], u[M], v[M], l[M], s[N], tot = 1, d = 0; 
int f[M], c[N], fw, bw;

void ae(int x, int y, int z)
{
    ++m;
    u[++tot] = x;
    v[tot] = y;
    f[tot] = z;
    l[tot] = h[x];
    h[x] = tot;
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
    // printf("%d %d %d\n", x, fl(x), ce(x));
    return x == fl(x) || x == ce(x);
}

int tr(int x, int y)
{
    return h[x] == y ? l[h[x]] : h[x];
}

void cnr(int x)
{
    if(f[x] == 0 || f[x] == one)
    {
        re(x);
        re(x ^ 1);
    }
}

int go(int x, int y, int p)
{
    if(s[x])
    {
        s[x] = 2;
        fw = bw = one;
        return 1;
    }

    s[x] = 1;
    
    if(y && p && (!in(c[x])))
    {
        s[x] = 2;
        fw = ce(c[x]) - c[x];
        bw = c[x] - fl(c[x]);
        return 1;
    }
    
    int t = tr(x, y);
    if(!t)
    {
        fw = bw = 0;
        return 0;
    }

    go(v[t], t ^ 1, p);
    fw = min(fw, f[t]);
    bw = min(bw, f[t ^ 1]);

    if(s[x] == 2 && fw + bw != 0)
    {
        int r;
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

        while(1)
        {
            f[t] -= r * d;
            c[v[t]] += r * d;
            f[t ^ 1] += r * d;
            c[u[t]] -= r * d;
            cnr(t);

            if(s[v[t]] == 2) break;
            t = tr(v[t], t ^ 1);
        }
        fw = bw = 0;
    }
    else if((!y) && p && fw + bw != 0)
    {
        fw = min(fw, c[x] - fl(c[x]));
        bw = min(bw, ce(c[x]) - c[x]);

        int r;
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

        while(1)
        {
            f[t] -= r * d;
            c[v[t]] += r * d;
            f[t ^ 1] += r * d;
            c[u[t]] -= r * d;
            cnr(t);

            if(s[v[t]] == 2) break;
            t = tr(v[t], t ^ 1);
        }
    }

    return 1;
}

int main()
{
    srand(time(0));
    rand();

    scanf("%d%d", &r, &p);
    n = p + r;

    int x, y, z;
    char sz[100];

    for(int i = 0; i < p * r; i++)
    {
        scanf("%d%d%s", &x, &y, sz);
        ++x;
        ++y;

        sz[dig + 2] = 0;
        sscanf(sz + 2, "%d", &z);
        for(int j = strlen(sz + 2); j < dig; j++) z *= 10;

        c[x] += z;
        c[y] -= z;
        if(z != 0)
        {
            ae(x, y, z);
            ae(y, x, one - z);
        }
    }

    while(m)
    {
        memset(s, 0, sizeof(s));
        for(int i = 1; i <= n; i++)
            if(!in(c[i]))
                if(go(i, 0, 1))
                    break;
        memset(s, 0, sizeof(s));
        for(int i = 1; i <= n; i++)
            if(go(i, 0, 0))
                break;
    }

    int count = 0;

    for(int i = 2; i <= tot; i++)
        if(u[i] < v[i] && f[i] == one)
            count += 1;

    printf("%d\n", count);

    for(int i = 2; i <= tot; i++)
        if(u[i] < v[i] && f[i] == one)
            printf("%d %d\n", u[i] - 1, v[i] - 1);

    return 0;
}
