# PNGToBlock
A tool that takes an image and generates a color coded image representing minecraft blocks that would best fit the sillouette

==========================================================================================================================================

PLEASE NOTE:

This tool can only process monochromatic (black/white) images with width and height that are multiples of 16 pixels.  The width and height
do not have to match for the program to work (16x32 is pefectly fine, but are still multiples of 16)

==========================================================================================================================================

To use this tool:

1) Compile the solution or use the provided release executable
2) Drag your executable and the folder: "PNGToSchem" into a folder and navigate to the folder using the command prompt
3) Enter the following command \<Name of executable\> \<Input image filepath\> \<Output image name\>
4) By adding the additional arguments \<-s\> \<output schematic name\> \<Plane (XY, YZ)\> \<FlipU?\> \<Flip V?\> \<Palette (not implemented yet!)\>
   you can output a schematic file for use in programs like World Edit.
  
If everything has been done correctly you'll see the program start processing your image

==========================================================================================================================================
  
Block Color codes:
  
wall:
  
    left (255, 0, 0) red
  
    center (0, 255, 0) green
  
    right (0, 0, 255) blue

wallpost:
  
    left (255, 255, 0) yellow
  
    right (0, 255, 255) cyan

trapdoor:
  
    left (0, 0, 0) black
  
    right (255, 255, 255) white
  
    top (255, 0, 255) magenta
  
    bottom (127, 0, 255) purple

stair:
  
    typej (0, 127, 255) sky blue
  
    typel (0, 255, 127) blue green
  
    type7 (127, 255, 0) yellow green
  
    typer (255, 127, 0) orange

fence closed:
  
    top (255, 0, 127) hot pink
  
    mid (127, 0, 0) maroon

fence opened:
  
    top_left (127, 127, 0) vomit
 
    mid_left (0, 127, 0) army green
  
    top_right (0, 127, 127) turquois
  
    mid_right (0, 0, 127) dark blue

piston:
  
    top (127, 0, 127) royal purple
  
    right(127, 127, 127) grey
  
    down(62, 0, 127) deep purple
  
    left(127, 0, 62) wine red

slab:
  
    top(189, 189, 189) light grey
  
    bottom(62, 62, 62) charcoal

full block:
  
    (0, 62, 0) dark green

air block:
  
    (190, 255, 255) light sky blue
