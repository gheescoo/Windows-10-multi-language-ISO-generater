ADK_PATH = 'C:\\Program Files (x86)\\Windows Kits\\10\\Assessment and Deployment Kit\\Deployment Tools\\'
WIM_path = 'sources\\install.wim'
BOOT_path = 'sources\\boot.wim'
RE_path = 'Windows\\System32\\Recovery\\winre.wim'

DISM_MOUNT = 'DISM /Mount-Image /ImageFile:{img} /Index:{idx} /MountDir:{mntdir}'
DISM_ADDPKG = 'DISM /Image:{mntdir} /Add-Package /PackagePath={pkg}'
DISM_ADDPAP = 'DISM /Image:{mntdir} /Add-ProvisionedAppxPackage /PackagePath={pkg} /LicensePath:{ca}'

DISM_UNMOUNT_COMMIT = 'DISM /Unmount-Image /MountDir:{mntdir} /Commit /CheckIntegrity /Append'
DISM_GENLANGINI = 'Dism /image:{img} /Gen-LangINI /distribution:{dis}'

XCOPY_LANGINI = 'XCOPY {src}\\sources\\lang.ini {dest}\\sources\\lang.ini'
