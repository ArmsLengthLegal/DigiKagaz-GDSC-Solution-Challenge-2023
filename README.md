
# DigiKagaz-GDSC Solution Challenge 2023

## About the Project

DigiKagaz is a self-help tool that addresses the challenges of limited resources and language barriers faced by indigent individuals seeking legal aid services in India. Our solution enables users to generate relevant legal documents quickly and easily, regardless of their language proficiency or financial situation.

Our team comprises individuals from diverse backgrounds, including legal and technology expertise. We have actively worked on two modules, namely the BAIL Module and the DOMESTIC VIOLENCE MODULE, to address critical issues that require urgent attention. Our modules can also help advocates doing pro bono work to increase their power to handle cases.

We have actively tested our solution with real users and have collected valuable feedback that we used to improve our solution. Our goals have been evidenced by the positive feedback we received from users and the increase in the number of users generating legal documents on our platform.

## Demo and URL

Demo Video: https://youtu.be/rM0OPdyiwSo

Android App URL: https://play.google.com/store/apps/details?id=com.digikagaz


## Installation

To deploy this project, install docker and run docassemble image using following commands:

```bash
sudo yum -y update
sudo yum -y install docker
sudo usermod -a -G docker ec2-user

docker run -d -p 80:80 -p 443:443 --stop-timeout 600 jhpyle/docassemble
```

Install our package as extention to Docassemble using following steps: 
- In the docassemble web app, go back to Package Management.
- Under "Zip File", upload the .zip file you want to install.
- Click "Update".

Refer [Documentation](https://docassemble.org/docs/packages.html#zip_install) for more info on installing package.

  
## Usage

Open the browser and point to the interview URL (http://localhost/interview?i=docassemble.DigiKagaz:data/questions/hazari_maafi.yml) to access the interview form.

    
