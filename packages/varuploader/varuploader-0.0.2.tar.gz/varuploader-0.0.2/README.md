<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<br />
<div align="center">
  <a href="https://github.com/dorta/var-uploader">
    <img src="docs/images/logo.png" alt="Logo">
  </a>

<h3 align="center">Recovery SD Card Uploader Tool</h3>

  <p align="center">
    Internal tool to help the R&D Software team upload new releases to the FTP
    <br />
    <a href="https://github.com/dorta/var-uploader/issues">Report Bug</a>
    ·
    <a href="https://github.com/dorta/var-uploader/issues">Request Feature</a>
  </p>
</div>

## About 

The Variscite Recovery SD Card Uploader tool helps the internal R&D Software
team upload new recovery SD cards releases to the [Variscite FTP](https://ftp.variscite.com/files) server,
automatically updating the changelog file in the [YAML](https://yaml.org/)
file format.

[![Product Name Screen Shot][product-screenshot]](https://example.com)

## 1. <a name='Getting Started'></a>Getting Started

### Supported OS

| OS                             | Arch   | Release | Status |
|--------------------------------|--------|---------|--------|
| Debian GNU/Linux 11 (bullseye) | x86_64 | 1.0.0   | Passed |
| Ubuntu GNU/Linux 22.04 LTS     | x86_64 | 1.0.0   | Passed |
| Mint GNU/Linux 21              | x86_64 | 1.0.0   |        |

### Prerequisites

#### Debian and Ubuntu

Install the following dependencies packages in the host system:
   ```sh
   apt install python3 python3-pip pyyaml
   ```

### Install via Pip Tool (Recommended)

To install the Recovery SD Card Uploader tool, use the pip tool:
   ```sh
   pip3 install varuploader
   ```

#### Important Notes

* You may need to export the following path: `export PATH="$HOME/.local/bin:$PATH"`

* The `varuploader` package is hosted on the [pypi.org](https://pypi.org/project/varuploader/) page.

* To manually build the tool, see this [building](https://github.com/dorta/var-uploader/tree/main/docs/build.md) guide.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 2. <a name='Usage'></a>Usage

To use the tool, run in the terminal:
   ```sh
   varuploader
   ```

### Create New Release

The following steps automatically updates the `changelog` file and uploads the
recovery SD card to the FTP:

1. Choose the recovery SD card to upload to the Variscite FTP, then press the **`Create New Release`** button.
    * __NOTE:__ The recovery SD card tool automatically renames the recovery SD card image.

2. Fill the fields according, then press the **`Export Release`** button:
    * __NOTE:__ The `date`, `path`, `sha224`, and the `file size` are automatically filled.

3. Review the information, then press the **`Ok`** button:

4. Enter the Variscite FTP credentials, then press the **`Ok`** button:
    * __NOTE:__ The `user` and `password` values are the FTP credentials with root
      permission that allows the _var-uploader_ tool to upload and update files in
      the FTP server. These credentials are managed by the R&D Software Team.

### Edit an Existing Release

Coming soon.

### Remove an Existing Release

Coming soon.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


## 3. <a name='Changelog and Roadmap'></a>Changelog and Roadmap

### Latest Release

* [1.0.0 - 2022-08-18 - Initial Release of the Variscite Recovery SD Card Uploader Tool](https://github.com/dorta/var-uploader/blob/main/CHANGELOG.md#100---2022-08-18)

See the full changelog file content at [here](https://github.com/dorta/var-uploader/blob/main/CHANGELOG.md).

### Next Releases

See the roadmap for the next features:

   | Feature                               | Release Version | Status    | Date       |
   |---------------------------------------|-----------------|-----------|------------|
   | Support for Yocto Releases            | 1.0.0           |  Passed   | 08/2022    |
   | Support for Debian Releases           |                 |           | 09/2022    |
   | Support for B2Qt Releases             |                 |           | 09/2022    |
   | Support to Create New Release         | 1.0.0           |  Passed   | 08/2022    |
   | Support to Edit an Existing Release   |                 |           | 10/2022    |
   | Support to Remove an Existing Release |                 |           | 10/2022    |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 4. <a name='Copyright and License'></a>Copyright and License

Copyright 2022 Variscite LTD. Free use of this software is granted under
the terms of the [BSD 3-Clause License](https://github.com/dorta/var-uploader/blob/master/LICENSE).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/dorta/var-uploader.svg?style=for-the-badge
[contributors-url]: https://github.com/dorta/var-uploader/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/dorta/var-uploader.svg?style=for-the-badge
[forks-url]: https://github.com/dorta/var-uploader/network/members
[stars-shield]: https://img.shields.io/github/stars/dorta/var-uploader.svg?style=for-the-badge
[stars-url]: https://github.com/dorta/var-uploader/stargazers
[issues-shield]: https://img.shields.io/github/issues/dorta/var-uploader.svg?style=for-the-badge
[issues-url]: https://github.com/dorta/var-uploader/issues
[license-shield]: https://img.shields.io/github/license/dorta/var-uploader.svg?style=for-the-badge
[license-url]: https://github.com/dorta/var-uploader/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/company/variscite-ltd-
[product-screenshot]: docs/images/main_window.png
