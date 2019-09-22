import git
import os
import pickle
import sys
import time
import zipfile

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
        args = self.args()

        if args['--flush'] == True:
            pickleh.destroy()
            pickleh.create()
        
        # check if branch_name is undefined
        self.checkBranchName()

        # check config keys exist
        self.latestCommit()
        
    def ret(self):
        return pickleh.get(pickleh)

    def checkBranchName(self):
        if len(pickleh.attr(pickleh, 'branch_name')) < 1:
            pickleh.store(pickleh, 'branch_name', 'master')

    def latestCommit(self):
        if len(pickleh.attr(pickleh, 'last_commit_zipped')) != 40:
            latest = input("Please enter a commit hash to compare from: ")
            if len(latest) != 40:
                print('Error: Hash should be 40 charchters length 👊')
                self.latestCommit()
            else:
                pickleh.store(pickleh, 'last_commit_zipped', latest)

    def args(self):
        arguments = {
            '--branch' : 'master',
            '--flush' : False,
        }

        for arg in sys.argv[1:]:
            name = arg.split('=')
            arguments[name[0]] = name[1] if len(name) > 1 else True

            if (name[0] == '--branch'):
                pickleh.store(pickleh, 'branch_name', arguments['--branch'])

        return arguments

# main function
class gitAmrography():
    def __init__(self):
        global repo
        global g
        global git_path
        global config
        global branch_name

        c = initConfig()
        config = c.ret()
        branch_name = config['branch_name']

        git_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        repo = git.Repo(git_path)
        g = git.Git(git_path)

    def gitLatestCommit(self):
        return str(repo.heads[branch_name].commit.tree)
        
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
        commits_length = len(commits)
        if commits_length > 0:
            self.packagePrepare(commits, latestcommit)
            print('\n🥳 Package is ready')
            print('⛓  Commits affected = ' + str(commits_length) )
        else:
            print('\n✅ No changes to package')
        print('🍴 Branch -> ' + branch_name)
    
    def packagePrepare(self, commits, latestcommit):
        new_archive_dir = "archives/" + branch_name + "_" + str(int(time.time()))
        if not os.path.exists(new_archive_dir):
            os.makedirs(new_archive_dir)
        zipf = zipfile.ZipFile(new_archive_dir + '/archive.zip', 'w', zipfile.ZIP_DEFLATED)
        self.packageAdd(commits, zipf, new_archive_dir)
        zipf.close()
        pickleh.store(pickleh, 'last_commit_zipped', latestcommit)

    def packageAdd(self, commits, ziph, archive_directory):
        deleted_file = archive_directory + "/deleted_files.txt"
        changed_file = archive_directory + "/changed_files.txt"
        fd = open(deleted_file ,"w+")
        fc = open(changed_file ,"w+")
        for commit in commits:
            file = "../" + commit
            if os.path.isfile(file):
                print('✅ File added ', commit)
                fc.write("%s\n" % (commit))
                ziph.write(file)
            else:
                print('❌ File deleted ', commit)
                fd.write("%s\n" % (commit))
        fd.close()
        fc.close()


archive = gitAmrography()
archive.package()
