##### Clear build history

Go to <b>Manage Jenkins > Script Console</b>.
Paste following script in the console and hit run.

```
def jobName = "Job_Name"
def job = Jenkins.instance.getItem(jobName)
job.getBuilds().each { it.delete() }
job.nextBuildNumber = 1
job.save()
```
