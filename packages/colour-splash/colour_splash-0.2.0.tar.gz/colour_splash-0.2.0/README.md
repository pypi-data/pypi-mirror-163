# Colour Splash
A simple tool enabling easy colouring of terminal outputs

# Download
## Using PIP to use a imported Module
`pip install colour_splash`
## Manually to embed into a project
`git clone https://github.com/lachlan2357/python-colour-splash` into your project directory

# Usage
Include `import colour_splash` at the top of your file

## Functions
### `colour_splash.colour()`
Changes the foreground, background or both-grounds of text
#### Parameters:
- `text` the text you wish to be coloured
- `foreground` (optional): the string value of the name of the colour you wish to use as the foreground (text) colour
- `background` (optional): the string value of the name of the colour you wish to use as the background (highlighted) colour

### `colour_splash.style()`
Changes the style of text
#### Parameters:
- `text`: the text you wish to be styled
- `style` (optional): the string value of the name of the style you wish to use

### `colour_splash.colour_start()`
Starts a specific colour for all proceeding text
#### Parameters:
- `foreground` (optional): the string value of the name of the colour you wish to use as the foreground (text) colour
- `background` (optional): the string value of the name of the colour you wish to use as the background (highlighted) colour

### `colour_splash.style_start()`
Starts a specific style for all proceeding text
#### Parameters:
- `style` (optional): the string value of the name of the style you wish to use

### `colour_splash.colour_end()`
Returns the proceeding text to its previous colour/style

### `colour_splash.style_end()`
Returns the proceeding text to its previous colour/style

### `colour_splash.help()`
Lists colours and styles and how they appear on your system