Most of the steps come from [Microsoft](https://learn.microsoft.com/).
<!--
[Benno Rummens' article](https://www.bennorummens.com/products/windows-10/how-to-create-a-multi-language-windows-10-image/). Actually he inspired me.
-->

# Prerequisites

* Files of [Windows 10 ISO](https://www.microsoft.com/en-us/software-download/windows10ISO)
  Use a user agent other than Windows NT if you don't want the Media Creation Tool.

* Files of [Multi Language Pack ISO and Features on Demand ISO](https://licensing.microsoft.com/)
  The Volume Licensing site may not be accessible for everyone. Use [MicrosoftDocs](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/virtual-desktop/language-packs.md) as a fallback. Try to put all ```.cab``` files into one folder if you only get ```.cab``` files.

* [Windows Assessment Deployment Kit](https://developer.microsoft.com/en-us/windows/hardware/windows-assessment-deployment-kit)
  Install following features:
  * Deployment Tools
  * Imaging And Configuration Designer (ICD)
  * Configuration Designer
  * User State Migration Tool (USMT)
  * \*If you want a multi-lingual Windows Setup, also install Windows PE add-on.

# Steps
  1. execute ```main.py```
  1. Specify the path Windows 10 ISO is extracted, which should be writable.
  2. Specify the path Multi Language Pack is extracted, which directly contains ```.cab``` files, and can be read-only.
  3. Specify the path of working folder. This path should be writable.
  4. Check your needs.
