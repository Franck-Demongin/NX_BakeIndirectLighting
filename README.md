![hero](https://user-images.githubusercontent.com/54265936/214667043-b3fcf270-7256-4257-a24e-5919d8c828ae.png)

<img src="https://img.shields.io/badge/Blender-3.0.0-green" /> <img src="https://img.shields.io/badge/Python-3.10-blue" /> <img src="https://img.shields.io/badge/Addon-1.1.0.Stable-orange" /> [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)

# NX_BakeIndirectLightning
Bake lndirect lightning before render image or animation with EEVEE

## Installation
Download ZIP file on your system.

In Blender, install addon from _Preferences > Add-ons > Install_...  
Activate the addon

## Usage

Select EEVEE has render engine.  
Create a scene with a Light Probe of type Irradiance Volume. 

### Bake Indirect Lighting and render frame
In menu Render > BIL and Render Image

Like a normal render but indirect lighting are baked before perform render.  
By default, the render is make in a new window. When render is finish, save the image like usual.

Shotcut : Alt F12

### Render animation and Bake Indirect Lighting before render each frame
In menu Render > BIL and Render Animation

Rendering the animation as a sequence of images. PNG, JPEG, BMP, TIFF, OpenEXR and WebP formats are available, select one in the Output Properties panel.  
Select a folder where the images will be saved.

Press ESC to cancel render.

Shortcut : Shift Alt F12

## Change Log

[1-1-0] - 2023-01-27

### Added

### Changed
- When rendering the animation, the editor used will be the last one opened in the window.  
It can be of any type except Outliner and Properties.
- When rendering is complete, the editor reverts to its original type.

### Fixed
