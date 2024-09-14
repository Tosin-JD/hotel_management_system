[Setup]
AppName= Guest House
AppVersion=1.0
DefaultDirName={pf}\GuestHouse
OutputDir=Output
OutputBaseFilename=GuestHouseSetup
Compression=lzma
SolidCompression=yes

[Files]
; Include the built executable
Source: "C:\Users\MFM INT'L HQ ANNEX\Documents\hms\build\exe.win-amd64-3.11\app.exe"; DestDir: "{app}"; Flags: ignoreversion
; Include any additional files your application needs

[Icons]
Name: "{group}\ Guest House"; Filename: "{app}\GuestHouse.exe"
; Create Start Menu shortcuts or desktop icons as needed

