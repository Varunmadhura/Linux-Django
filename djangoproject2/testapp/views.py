from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import paramiko

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('scenario2')
    return render(request, "testapp/login.html")

def scenario2(request):
    return render(request, "testapp/page2.html")

def execute_command(request):
    if request.method == 'POST':
        hostname = request.POST.get('hostname', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        commands = [
            request.POST.get('command1', ''),
            request.POST.get('command2', ''),
            request.POST.get('command3', ''),
            request.POST.get('command4', ''),
            request.POST.get('command5', '')
        ]

        outputs = []
        error = ""

        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=hostname, username=username, password=password)

            for command in filter(None, commands):
                stdin, stdout, stderr = ssh_client.exec_command(command)
                exit_status = stdout.channel.recv_exit_status()

                if exit_status == 0:
                    output = stdout.read().decode('utf-8').strip()
                    outputs.append(output)
                else:
                    error = stderr.read().decode('utf-8').strip()
                    outputs.append(f"Error executing {command}: {error}")
                    error = "Stop execution due to failed command"
                    break

            ssh_client.close()

        except paramiko.AuthenticationException:
            error = "Authentication failed. Please check your credentials."
        except Exception as e:
            error = f"An error occurred: {str(e)}"

        return render(request, 'testapp/page2.html', {'outputs': outputs, 'error': error})

    return render(request, 'testapp/page2.html')
