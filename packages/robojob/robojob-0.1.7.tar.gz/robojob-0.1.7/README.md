# Quickstart

Install robojob using `pip install robojob`.

## Hello, world

First, try importing robojob and executing a simple Python task.

Save the following as `hello.py` and run it:

~~~python
import robojob

def greet(name):
    print(f"Hello, {name}!")

with robojob.go("hello") as ctx:
    ctx.execute(greet, name="world")
~~~

The result is the same as calling `greet(name="world")`.

Next, turn on logging by adding the following (above the `with` statement):

~~~python
import logging

logging.basicConfig(level="INFO", format="[%(levelname)s] %(message)s")
~~~

Running the script again, you can see the logging output from robojob:

~~~
[INFO] Job starting: <JobExecution: 55821589-750d-4c0c-9c1e-9d10570fd47f>
[INFO] Task starting: <FunctionExecution: greet>
Hello, world!
[INFO] Task completed with status Completed
[INFO] Running time: 0:00:00.000995
[INFO] Job completed with status Completed
[INFO] Running time: 0:00:00.001995
~~~

Task and job executions are timed and the status each is tracked logged. If you change the log level to "DEBUG", you can see the parameter values assigned, too.

The remainder of the tutorial covers three topics:

- How robojob handles failed tasks and jobs.
- How to use a configuration file to separate parameter values (and other configuration details) from job definitions.
- How to use a backend to log task and job executions to a central location.

## Failure

Try making the "orchestration" part of the code fail (by not passing a value for the `name` paramter):

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(greet)
~~~

The error gets logged along with the stack trace before being reraised:

~~~
[INFO] Job starting: <JobExecution: 339fe025-35db-4195-a6ee-3d9a6b571662>
[ERROR] Job failed: "The parameter 'name' is not defined."
  File "hello.py", line 11, in <module>
    ctx.execute(greet)
   ...
[INFO] Job ended with status Failed
[INFO] Running time: 0:00:00
~~~

Next, add a task that fails:

~~~python
def fail():
    print(1/0)
~~~

Modify the job to call the task:

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(fail)
~~~

Now, both the failure of the task and job are logged:

~~~
[INFO] Job starting: <JobExecution: a008efa1-5352-45f7-b424-fd21dcdda9f7>
[INFO] Task starting: <FunctionExecution: fail>
[ERROR] Task failed: division by zero
[INFO] Task completed with status Failed
[INFO] Running time: 0:00:00.000995
[ERROR] Job failed: division by zero
  File "c:\Users\frs\source\repos\robojob\hello.py", line 14, in <module>
    ctx.execute(fail)
    ...
[INFO] Job completed  with status Failed
[INFO] Running time: 0:00:00.003990
~~~

You can define a task that is invoked when the job fails:

~~~python
def handle_error(job_execution_id):
    print(f"Job {job_execution_id} failed :-(")
~~~

You need to register the task with the job execution context:

~~~python
with robojob.go("hello") as ctx:
    ctx.add_error_handler(handle_error)
    ctx.execute(fail)
~~~

The error handler uses the built-in parameter `job_execution_id` [MERE].

Sending email to notify operators of errors can be done with `add_error_email()`

## Using a configuration file

Until now, we've passed parameter values in the call to execute:

~~~python
with robojob.go("hello") as ctx:
    ctx["name"] = "world"
    ctx.execute(greet)
~~~

Variables can also be assigned as part of job execution initialization:

~~~python
with robojob.go("hello", parameters={"name": "world"}) as ctx:
    ctx.execute(greet)
~~~

Or moved to a YAML configuration file:

~~~yaml
# robojob.yml
parameters:
  name: world
~~~

This makes the Python code even simpler:

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(greet)
~~~

If a parameter is added to a task, robojob will bind the parameter to a value, with no change to the job definition:

~~~python
def greet(job_name, name):
    print(f"Hello from {job_name}, {name}!")
~~~

The `job_name` parameter is built in - it stores the name of the currently running job. The built-in parameters are:
- `id`: The GUID identifying the currently running job.
- `job_name`: The name of the job.
- `environment_name`: The name of the environment.
- `status`: The current status of the job.
- `error_message`: If the job has failed, this is the error message - this is primarily useful for error handling tasks.

## Using a backend

Since all task configuration, execution and orchestration happens through the job execution context, robojob can log job and task executions to a backend.

Setting up a backend in SQL Server requires a few tables:

~~~sql
CREATE DATABASE Robojob
GO

USE Robojob
GO

CREATE TABLE dbo.JobExecution (
	JobExecutionGUID UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
	JobExecutionID INT NOT NULL IDENTITY(1,1),
	EnvironmentName NVARCHAR(20) NOT NULL,
	JobName NVARCHAR(255) NOT NULL,
	ExecutedBy SYSNAME NOT NULL DEFAULT SUSER_SNAME(),
	StartedOn DATETIME2(3) NOT NULL,
	CompletedOn DATETIME2(3) NULL,
	[Status] NVARCHAR(20) NULL,
	ErrorMessage NVARCHAR(MAX) NULL,
  )
GO

CREATE TABLE dbo.TaskExecution (
  TaskExecutionGUID UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
  JobExecutionGUID UNIQUEIDENTIFIER NOT NULL,
  TaskTypeName NVARCHAR(255) NOT NULL,
  TaskName NVARCHAR(255) NOT NULL,
  ExecutedBy SYSNAME NOT NULL DEFAULT SUSER_SNAME(),
  StartedOn DATETIME2(3) NOT NULL,
  CompletedOn DATETIME2(3) NULL,
  [Status] NVARCHAR(20) NOT NULL,
  ErrorMessage NVARCHAR(MAX) NULL,
  )
GO

CREATE TABLE dbo.TaskExecutionParameter (
  TaskExecutionGUID UNIQUEIDENTIFIER NOT NULL,
  ParameterName NVARCHAR(50) NOT NULL,
  ParameterValue NVARCHAR(4000) NOT NULL,
  PRIMARY KEY ( TaskExecutionGUID, ParameterName )
  )
GO

CREATE TABLE dbo.Hello (
  JobExecutionID INT NOT NULL,
  [Message] NVARCHAR(100) NOT NULL
)

GO

CREATE PROCEDURE dbo.SayHello @JobExecutionID INT, @Name NVARCHAR(50)
AS
INSERT INTO dbo.Hello (JobExecutionID, [Message])
VALUES (@JobExecutionID, 'Hello ' + @Name)

~~~



~~~python
backend = SqlServerBackend(pyodbc.connect("<connection string>", autocommit=True))

with robojob.go("hello", backend=backend) as ctx:
    ctx.execute(greet)
~~~

You can configure the backend in the configuration file, too:

~~~yaml
backend:
  type: sql server
  connection string: <connection string>
~~~

# Features

- *Job definition as code:* Jobs are Python code wrapped in a context manager.
- *Job configuration as data:* Parameter values can be stored in a configuration file.
- *Dynamic parameter binding:* Parameter values are wired to tasks at runtime, so adding a parameter to a task (e.g. a stored procedure) will work with no change to the job definition code.
- *Logging*: Parameter values used and errors raised by tasks are logged, and so are error thrown by the orchestration parts of the job.

# Interface

## Task execution
The main part of the job execution context interface is the methods for executing tasks. A number of convenience methods are provided for this.

- Python functions:
  - `ctx.execute(do_stuff)` executes the python function `dostuff`, binding parameter values by name.
- SQL Server stored procedures:
  - `ctx.execute_procedure(conn, "dbo", "LoadStuff")` executes the stored procedure `dbo.LoadStuff` using the connection `conn`, binding parameters by name (parameter name matching is fuzzy, so the `@` character and casing are both  ignored).
  - `ctx.execute_procedure(conn, "dbo", "LoadStuff", "LoadMoreStuff")` executes two stored procedures in the `dbo` schema.
- R scripts:
  - `ctx.execute_r("DoStuff.R")` executes the script named "DoStuff.R". Parameters are passed by inspecting the first line of the script and looking for parameter names (consisting of letters, numbers and underscores, e.g. `# first_parameter - second_parameter`) and then calling the R script with the value of the named parameters as arguments, in the order listed.
  - `ctx.execute_r("DoStuff.R", "DoMoreStuff.R")` executes two scripts.
- Email:
  - `ctx.send_email(sender, recipients, subject, content)` sends an email. The name of an available SMTP server must be registered in the `smtp_server` context variable. `subject`and `content` are both treated as [string templates](https://docs.python.org/3/library/string.html#template-strings) with parameter values from the job execution context being substituted when the mail is sent.

Note: All these methods call `ctx.process_task_execution(task)` one or more times. Custom tasks can be implemented by subclassing `TaskExecution` and passing instances of the task execution class to `process_task_execution()`. Tasks are also used for error handling: Assigning a task execution instance to `ctx.on_error` will cause the task to be executed immediately before job execution ends, if an error occurs.


## Parameters

The job execution context stores parameter values and implements a subset of the Python dictionary interface:
- `ctx["param"] = "world"` assigns the value "world" to the parameter named "param".
- `ctx["param"]` returns the value of the parameter named "param"
- `ctx.get("param")` returns the value of the parameter named "param" or None, if the parameter is undefined.
- `ctx.get("param", "default_value")` returns the value of the parameter named "param", if the parameter is undefined and "default_value" otherwise.
- `"param" in ctx` returns True if the context contains a parameter named "param", False otherwise

The following job execution parameters are built in and their value cannot be changed:

- `id`: the GUID identifying this job execution.
- `job name`: the name of the job.
- `environment name`: the name of the environment that the job is running in.
- `status`: the current status of the job.
- `error message`: if the job has failed, this contains an error message. This is primarily useful in error handling tasks

(The SQL Server backend will add the integer-valued `job execution id` to the job execution context.)

## Other methods
The job execution context has a few utility functions:
- `ctx.export("param")` makes the current value of the parameter named "param" available in the environment of subprocesses spawned by robojob.
- `ctx.exit()` exits the job immediately, setting the status of the job to "Completed"
- `ctx.exit(status="Skipped")` exits the job immediately, setting the status of the job to "Skipped"
- `ctx.add_error_email(sender, recipients, subject, content, recipients_cc=[])` adds an email error handler. If the job fails, email will be sent using the SMTP server named in the `smtp_server` context parameter.


Set up logging to see what's happening behind the scenes:

~~~python
import logging

logging.basicConfig(level="INFO", format="%(levelname)s %(message)s")
~~~

Here we can see the job and task execution numbers - but until you connect robojob to a proper backend, the numbers will be assigned sequentially and task and job executions will not be logged.

## Setting a context parameter

Try moving a parameter value to the job execution context:

~~~python
with robojob.go("hello") as ctx:
    ctx["name"] = "world"
    ctx.execute(greet)
~~~

Note that the parameter value still gets used, even though it is not passed directly.

# Using config files

Now try moving the parameter value to a configuration file called `robojob.yml`, in the same directory as the script:

~~~yaml
parameters:
  name: fileworld
~~~

Then remove the parameter value from the job definition:

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(greet)
~~~

## Using the job execution id

Try adding a new task:

~~~python
def greet_again(name, job_execution_id):
    print(f"Hello again from {job_execution_id}, {name}!")
~~~

Then add it to the job:

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(greet)
    ctx.execute(greet_again)
~~~

Notice that `greet_again` can access the job execution ID even though it was not passed or added explicitly anywhere.

## Exiting early from a job

You can use the `exit()` method of the job execution context to exit early from a job.

~~~python
with robojob.go("hello") as ctx:
    ctx.execute(greet)
    ctx.exit("Skipped")
    ctx.execute(greet_again)
~~~

`exit()` is primarily useful for jobs that sometimes run without doing anything other than checking if they should do something.

You can supply a custom status to make it clear that the job ended abnormally, but
`exit()` should not be used when an error has occurred. In this case, you should throw 
an exception, which will propagate to whatever invokes the job.

# Details

## Job Execution

1) The job execution passes itself to the backend where it is logged and assigned a job execution id.
1) Orchestration code and tasks are executed, with parameter values and logging being  managed by the job execution.
1) When control passes out of the context, the job execution checks how the job ended:
- If a `UserExitException` was thrown, the status of the job is changed to the status passed with exception and the error is suppressed.
- If any other exception was thrown, the status is changed to "Failed" and the error is rethrown.
- Otherwise, the status is changed to "Completed". In any case, the job execution finally passes itself to the backend for logging.

## Task execution

The `execute()` method executes Python functions in the parameter and logging context of a job execution. There are several other job 
- `execute_procedure()` executes SQL Server stored procedures
- `execute_r()` executes an R script, passing the parameters named in the first line of the script. Parameter names are all sequences of alphanumerical characters and underscores.
- `execute_powershell()` executed a PowerShell script, passing the parameters passed in the `param()` declaration of the script (which must be kept on the first line).

These are all convenience methods that set up a `TaskExecution` instance and pass it to `process_task_execution()`, which performs parameter binding and starts the task, catching exceptions and logging along the way. 

1) The client creates a Task Execution instance that hold the details of the task being executed and passes it to the `process_task_execution` of the Job Execution context.
1) Parameter binding:
  - The Job Execution context creates a Parameter Collection holding the parameter values that will be accessible to the task execution. This is a combination of global variables and local variables supplied for this particular task execution.
  - The Task Execution instance uses the Parameter Collection to bind specific 
1) Logging: The job and task execution instances are passed to the backend, which logs 
   The task execution id is assigned after parameter binding and is therefore not accessible to tasks.
1) Execution:
  - The job execution context tries to execute the task execution instance
  - If an exception is raised, the status of the task is changed to "Failed" and the error is message is attached to the task execution instance before it is passed to the backend for logging and the error is rethrown.
  - If no error is thrown, the status of the task is changed to "Completed" before it is passed to the backend for logging

