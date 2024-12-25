# SpriteBinder

SpriteBinder allows you to easily manage and combine multiple individual sprites or sprite sheets into a single sprite sheet.

## Key Features
1. **Image Selection**: Choose multiple images at once using a simple file selection dialog.
2. **Horizontal/Vertical Sprite Sheet**: Organize your images horizontally or vertically to create the perfect sprite sheet for your needs.
3. **Preview & Edit**: View selected images on an interactive canvas and rearrange them using up/down buttons.
4. **Export**: Save the combined sprite sheet in popular formats (PNG, JPEG) with transparent or solid backgrounds.
5. **Tested on**: Fedora

## Table of Contents
- [Installation](#installation)
- [License](#license)

## Installation

To get started, follow the instructions below to install the necessary libraries and build the project.

### Step 1: Install Dependencies

First, you'll need to install the required Python libraries. You can do this using `pip`.

#### Install pillow
pillow is a popular Python Imaging Library used for image processing.

```bash
pip install pillow

#### Install pyinstaller
To build executable

```bash
pip install pyinstaller

### Step 2: Clone repository and go to main.py directory of the clone.

```bash
cd src

### Step 3: Run this command to build executable. In linux icon is ignoring.

```bash
pyinstaller --onefile --icon=Icon.ico main.py

### Step 4: Run the executable
./dist/main



