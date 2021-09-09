# Drawing On Canvas

There are two alternatives to doing awkward DOM manipulation with regular HTML elements. The first is DOM-based but utilizes _Scalable Vector Graphics_ (SVG), rather than HTML. Think of SVG as a document-markup dialect that focuses on shapes rather than text. You can embed an SVG document directly in an HTML document or include it with an `<img>` tag.

The second alternative is called a _canvas_. A canvas is a single DOM element that encapsulates a picture. It provides a programming interface for drawing shapes onto the space taken up by the node. The main difference between a canvas and an SVG picture is that in SVG the original description of the shapes is preserved so that they can be moved or resized at any time. A canvas, on the other hand, converts the shapes to pixels (colored dots on a raster) as soon as they are drawn and does not remember what these pixels represent. The only way to move a shape on a canvas is to clear the canvas (or the part of the canvas around the shape) and redraw it with the shape in a new position.

## SVG

This is an HTML document with a simple SVG picture in it:

```html
<p>Normal HTML here.</p>

<svg xmlns="http://www.w3.org/2000/svg">
  <circle r="50" cx="50" cy="50" fill="red" />
  <rect x="120" y="5" width="90" height="90" stroke="blue" fill="none" />
</svg>
```

The `xmlns` attribute changes an element (and its children) to a different XML _namespace_. This namespace, identified by a URL, specifies the dialect that we are currently speaking. The `<circle>` and `<rect>` tags, which do not exist in HTML, do have a meaning in SVG — they draw shapes using the style and position specified by their attributes.

## The Canvas Element

The `<canvas>` tag is intended to allow different styles of drawing. To get access to an actual drawing interface, we first need to create a context, an object whose methods provide the drawing interface. There are currently two widely supported drawing styles: `2d` for two-dimensional graphics and `webgl` for three-dimensional graphics through the OpenGL interface.

You create a context with the `getContext` method on the `<canvas>` DOM element.

```html
<p>Before canvas.</p>
<canvas width="120" height="60"></canvas>
<p>After canvas.</p>

<script>
  let canvas = document.querySelector("canvas");
  let context = canvas.getContext("2d");
  context.fillStyle = "red";
  context.fillRect(10, 10, 100, 50);
</script>
```

Just like in HTML (and SVG), the coordinate system that the canvas uses puts (0,0) at the top-left corner, and the positive y-axis goes down from there. So (10,10) is 10 pixels below and to the right of the top-left corner.

## Lines and Surfaces

The `fillRect` method fills a rectangle. It takes first the x- and y-coordinates of the rectangle’s top-left corner, then its width, and then its height. A similar method, `strokeRect`, draws the outline of a rectangle.

The `fillStyle` property controls the way shapes are filled. It can be set to a string that specifies a color, using the color notation used by CSS.

The `strokeStyle` property works similarly but determines the color used for a stroked line. The width of that line is determined by the `lineWidth` property, which may contain any positive number.

## Paths

A path is a sequence of lines. The 2D canvas interface describes paths entirely through side effects.

Each segment created with `lineTo` starts at the path’s current position. That position is usually the end of the last segment, unless `moveTo` was called. In that case, the next segment would start at the position passed to `moveTo`.

When filling a path (using the `fill` method), each shape is filled separately. A path can contain multiple shapes (each `moveTo` motion starts a new one), but the path needs to be _closed_ (meaning its start and end are in the same position) before it can be filled. If the path is not already closed, a line is added from its end to its start, and the shape enclosed by the completed path is filled.

```html
<canvas></canvas>

<script>
  let cx = document.querySelector("canvas").getContext("2d");
  cx.beginPath();
  cx.moveTo(50, 10);
  cx.lineTo(10, 70);
  cx.lineTo(90, 70);
  cx.fill();
</script>
```

## Curves

The `quadraticCurveTo` method draws a curve to a given point. To determine the curvature of the line, the method is given a control point as well as a destination point. Imagine this control point as _attracting_ the line, giving it its curve. The line won’t go through the control point, but its direction at the start and end points will be such that a straight line in that direction would point toward the control point.

The `bezierCurveTo` method draws a similar kind of curve. Instead of a single control point, this one has two (one for each of the line’s endpoints). The two control points specify the direction at both ends of the curve. The farther they are away from their corresponding point, the more the curve will “bulge” in that direction.

The `arc` method is a way to draw a line that curves along the edge of a circle. It takes a pair of coordinates for the arc’s center, a radius, and then a start angle and end angle.

Those last two parameters make it possible to draw only part of the circle. The angles are measured in radians, not degrees. This means a full circle has an angle of `2π`, or `2 * Math.PI`, which is about `6.28`. The angle starts counting at the point to the right of the circle’s center and goes clockwise from there.

Like other path-drawing methods, a line drawn with arc is connected to the previous path segment. You can call `moveTo` or start a new path to avoid this.

## Text

A 2D canvas drawing context provides the methods `fillText` and `strokeText`. You can specify the size, style, and font of the text with the `font` property.

```html
<canvas></canvas>

<script>
  let cx = document.querySelector("canvas").getContext("2d");
  cx.font = "28px Georgia";
  cx.fillStyle = "fuchsia";
  cx.fillText("I can draw text, too!", 10, 50);
</script>
```

The last two arguments to `fillText` and `strokeText` provide the position at which the font is drawn. By default, they indicate the position of the start of the text’s alphabetic baseline, which is the line that letters “stand” on, not counting hanging parts in letters such as `j` or `p`. You can change the horizontal position by setting the `textAlign` property to "`end`" or "`center`" and the vertical position by setting `textBaseline` to "`top`", "`middle`", or "`bottom`".

## Images

In computer graphics, a distinction is often made between _vector_ graphics and _bitmap_ graphics. Bitmap graphics, on the other hand, don’t specify actual shapes but rather work with pixel data (rasters of colored dots).

The `drawImage` method allows us to draw pixel data onto a canvas. This pixel data can originate from an `<img>` element or from another canvas.

```html
<canvas></canvas>

<script>
  /*
  The following example creates a detached <img> element and loads an image file into it, but it cannot immediately start drawing from this picture because the browser may not have loaded it yet. To deal with this, we register a "load" event handler and do the drawing after the image has loaded.
  */
  let cx = document.querySelector("canvas").getContext("2d");
  let img = document.createElement("img");
  img.src = "img/hat.png";
  img.addEventListener("load", () => {
    for (let x = 10; x < 200; x += 30) {
      cx.drawImage(img, x, 10);
    }
  });
</script>
```

By default, `drawImage` will draw the image at its original size. You can also give it two additional arguments to set a different width and height.

When `drawImage` is given _nine_ arguments, it can be used to draw only a fragment of an image. The second through fifth arguments indicate the rectangle (x, y, width, and height) in the source image that should be copied, and the sixth to ninth arguments give the rectangle (on the canvas) into which it should be copied.

This can be used to pack multiple _sprites_ (image elements) into a single image file and then draw only the part you need.

To animate a picture on a canvas, the `clearRect` method is useful. It resembles `fillRect`, but instead of coloring the rectangle, it makes it transparent, removing the previously drawn pixels.

```html
<canvas></canvas>

<script>
  /*
  We know that each sprite, each subpicture, is 24 pixels wide and 30 pixels high. The following code loads the image and then sets up an interval (repeated timer) to draw the next frame.
  */
  let cx = document.querySelector("canvas").getContext("2d");
  let img = document.createElement("img");
  img.src = "img/player.png";
  let spriteW = 24,
    spriteH = 30;
  img.addEventListener("load", () => {
    let cycle = 0;
    setInterval(() => {
      cx.clearRect(0, 0, spriteW, spriteH);
      cx.drawImage(
        img,
        // Source rectangle
        cycle * spriteW,
        0,
        spriteW,
        spriteH,
        // Destination rectangle
        0,
        0,
        spriteW,
        spriteH
      );
      cycle = (cycle + 1) % 8;
    }, 120);
  });
</script>
```

## Transformation

Calling the `scale` method will cause anything drawn after it to be scaled. This method takes two parameters, one to set a horizontal scale and one to set a vertical scale.

Scaling by a negative amount will flip the picture around. The flipping happens around point (0,0), which means it will also flip the direction of the coordinate system. When a horizontal scaling of -1 is applied, a shape drawn at x position 100 will end up at what used to be position -100.

You can rotate subsequently drawn shapes with the rotate method and move them with the `translate` method. The interesting (and confusing) thing is that these transformations _stack_, meaning that each one happens relative to the previous transformations.

To flip a picture around the vertical line at a given x position, we can do the following:

```js
function flipHorizontally(context, around) {
  context.translate(around, 0);
  context.scale(-1, 1);
  context.translate(-around, 0);
}
```

We move the y-axis to where we want our mirror to be, apply the mirroring, and finally move the y-axis back to its proper place in the mirrored universe.

## Storing and Clearing Transformations

The `save` and restore methods on the 2D canvas context `do` this transformation management. They conceptually keep a stack of transformation states. When you call `save`, the current state is pushed onto the stack. When you call `restore`, the state on top of the stack is taken off and used as the context’s current transformation. You can also call `resetTransform` to fully reset the transformation.
