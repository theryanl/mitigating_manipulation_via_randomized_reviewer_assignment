# get the dataset name from the filename (removing extension and folders)
def get_dataset_name(name):
    s = name.find('/')
    e = name.find('.')
    return name[s+1:e]
