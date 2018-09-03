import git
import os
import pickle
import sys
import time
import zipfile

# join arguments to search them
argus = " ".join(sys.argv)
# script variables
config_file_name = 'store.pckl'

# handle the config file
class pickleh():
    def get(self):
        if not os.path.isfile(config_file_name):
            self.create()
        f = open(config_file_name, 'rb')
        config = pickle.load(f)
        f.close()
        return config
    def store(self, attr, value):
        config = self.get(self)
        config[attr] = value
        f = open(config_file_name, 'wb')
        pickle.dump(config, f)
        f.close()
        return config
    def attr(self, attr):
        config = self.get(self)
        return config.get(attr, '')
    def destroy():
        os.remove(config_file_name)
    def create():
        f = open(config_file_name, 'wb')
        pickle.dump({}, f)
        f.close()

# check config keys existence
class initConfig():
    def __init__(self):
        if argus.find('--flush') > -1:
            pickleh.destroy()
            pickleh.create()
        
        # check config keys exist
        self.latestCommit()
        
    def ret(self):
        return pickleh.get(pickleh)

    def latestCommit(self):
        if len(pickleh.attr(pickleh, 'last_commit_zipped')) != 40:
            latest = input("Please enter a commit hash to compare from: ")
            if len(latest) != 40:
                print('Error: Hash should be 40 charchters length 👊')
                self.latestCommit()
            else:
                pickleh.store(pickleh, 'last_commit_zipped', latest)

# main function
class gitAmrography():
    def __init__(self):
        global repo
        global g
        global git_path
        global config

        c = initConfig()
        config = c.ret()
        git_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        repo = git.Repo(git_path)
        g = git.Git(git_path)

    def gitLatestCommit(self):
        return str(repo.heads.master.commit.tree)
        
    def gitDiff(self, branch1, branch2):
        format = '--name-only'
        commits = []
        differ = g.diff('%s..%s' % (branch1, branch2), format).split("\n")
        for line in differ:
            if len(line):
                commits.append(line)
        return commits

    def package(self):
        latestcommit = self.gitLatestCommit()
        commits = self.gitDiff(latestcommit, config['last_commit_zipped'])
        if len(commits) > 0:
            self.packagePrepare(commits, latestcommit)
        else:
            print('No changes to package ✅')
    
    def packagePrepare(self, commits, latestcommit):
        new_archive_dir = "archives/" + str(int(time.time()))
        if not os.path.exists(new_archive_dir):
            os.makedirs(new_archive_dir)
        zipf = zipfile.ZipFile(new_archive_dir + '/archive.zip', 'w', zipfile.ZIP_DEFLATED)
        self.packageAdd(commits, zipf)
        zipf.close()
        pickleh.store(pickleh, 'last_commit_zipped', latestcommit)

    def packageAdd(self, commits, ziph):
        for commit in commits:
            file = git_path + "/" + commit
            file = "../" + commit
            if os.path.isfile(file):
                ziph.write(file)


archive = gitAmrography()
archive.package()