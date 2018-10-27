##### Revert commit

If you want remove files in the last commit, you can use this:

```
git reset --hard HEAD~1
```

If you need files in the last commit, you can use this:

```
git reset --soft HEAD~1
```


##### Forcefully push the commit to remote

Note: this helps when you have reverted commit locally and want them to push

```
git push -f
```


##### Resolve the merge conflicts while get pull

1. ``` git pull ```

2. If error occurs then go to step 3 else got to step 7

3. ``` git stash ```

4. Again 

   ``` git pull ```

   Note: at this stage your local changes will be removed and they are already stashed so get this back

5. ``` git stash apply --index ``` 

   If this not work 
   
   ``` git stash apply ```
   
   Note: at this stage your local and remote changes will be merged automatically and if git can not merge automatically
   then it shows both changes in file and you have to remove the merge conflicts manually

6. If you see the both modified files in ``` git status ``` then stage these file by ``` git add <file name> ```

7. You can commit your changes
