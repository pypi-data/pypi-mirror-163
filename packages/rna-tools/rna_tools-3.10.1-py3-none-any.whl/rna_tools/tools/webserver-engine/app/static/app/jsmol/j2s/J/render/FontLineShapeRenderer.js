Clazz.declarePackage ("J.render");
Clazz.load (["J.render.ShapeRenderer", "JU.P3", "$.P3i", "$.V3"], "J.render.FontLineShapeRenderer", ["java.lang.Float", "JU.PT", "J.c.AXES"], function () {
c$ = Clazz.decorateAsClass (function () {
this.imageFontScaling = 0;
this.atomA = null;
this.atomB = null;
this.font3d = null;
this.pt0i = null;
this.pt1i = null;
this.pt2i = null;
this.s1 = null;
this.s2 = null;
this.pointT = null;
this.pointT2 = null;
this.pointT3 = null;
this.vectorT = null;
this.vectorT2 = null;
this.vectorT3 = null;
this.tickInfo = null;
this.draw000 = true;
this.width = 0;
this.endcap = 3;
this.colixA = 0;
this.colixB = 0;
this.dotsOrDashes = false;
this.dashDots = null;
this.asLineOnly = false;
Clazz.instantialize (this, arguments);
}, J.render, "FontLineShapeRenderer", J.render.ShapeRenderer);
Clazz.prepareFields (c$, function () {
this.pt0i =  new JU.P3i ();
this.pt1i =  new JU.P3i ();
this.pt2i =  new JU.P3i ();
this.s1 =  new JU.P3i ();
this.s2 =  new JU.P3i ();
this.pointT =  new JU.P3 ();
this.pointT2 =  new JU.P3 ();
this.pointT3 =  new JU.P3 ();
this.vectorT =  new JU.V3 ();
this.vectorT2 =  new JU.V3 ();
this.vectorT3 =  new JU.V3 ();
});
Clazz.defineMethod (c$, "getDiameter", 
function (z, madOrPixels) {
var diameter;
var isMad = (madOrPixels > 20);
switch (this.exportType) {
case 1:
diameter = (isMad ? madOrPixels : Clazz.doubleToInt (Math.floor (this.vwr.tm.unscaleToScreen (z, madOrPixels * 2) * 1000)));
break;
default:
if (isMad) {
diameter = Clazz.floatToInt (this.vwr.tm.scaleToScreen (z, madOrPixels));
} else {
if (this.g3d.isAntialiased ()) madOrPixels += madOrPixels;
diameter = madOrPixels;
}}
return diameter;
}, "~N,~N");
Clazz.defineMethod (c$, "renderLine", 
function (p0, p1, diameter, pt0, pt1, drawTicks) {
pt0.set (Clazz.doubleToInt (Math.floor (p0.x)), Clazz.doubleToInt (Math.floor (p0.y)), Clazz.doubleToInt (Math.floor (p0.z)));
pt1.set (Clazz.doubleToInt (Math.floor (p1.x)), Clazz.doubleToInt (Math.floor (p1.y)), Clazz.doubleToInt (Math.floor (p1.z)));
if (diameter < 0) this.g3d.drawDottedLine (pt0, pt1);
 else this.g3d.fillCylinder (this.endcap, diameter, pt0, pt1);
if (!drawTicks || this.tickInfo == null) return;
this.atomA.sX = pt0.x;
this.atomA.sY = pt0.y;
this.atomA.sZ = pt0.z;
this.atomB.sX = pt1.x;
this.atomB.sY = pt1.y;
this.atomB.sZ = pt1.z;
this.drawTicks (this.atomA, this.atomB, diameter, true);
}, "JU.P3,JU.P3,~N,JU.P3i,JU.P3i,~B");
Clazz.defineMethod (c$, "drawTicks", 
function (pt1, pt2, diameter, withLabels) {
if (Float.isNaN (this.tickInfo.first)) this.tickInfo.first = 0;
this.drawTicks2 (pt1, pt2, this.tickInfo.ticks.x, 8, diameter, (!withLabels ? null : this.tickInfo.tickLabelFormats == null ? ["%0.2f"] : this.tickInfo.tickLabelFormats));
this.drawTicks2 (pt1, pt2, this.tickInfo.ticks.y, 4, diameter, null);
this.drawTicks2 (pt1, pt2, this.tickInfo.ticks.z, 2, diameter, null);
}, "JU.Point3fi,JU.Point3fi,~N,~B");
Clazz.defineMethod (c$, "drawTicks2", 
 function (ptA, ptB, dx, length, diameter, formats) {
if (dx == 0) return;
if (this.g3d.isAntialiased ()) length *= 2;
this.vectorT2.set (ptB.sX, ptB.sY, 0);
this.vectorT.set (ptA.sX, ptA.sY, 0);
this.vectorT2.sub (this.vectorT);
if (this.vectorT2.length () < 50) return;
var signFactor = this.tickInfo.signFactor;
this.vectorT.sub2 (ptB, ptA);
var d0 = this.vectorT.length ();
if (this.tickInfo.scale != null) {
if (Float.isNaN (this.tickInfo.scale.x)) {
var a = this.vwr.getUnitCellInfo (0);
if (!Float.isNaN (a)) this.vectorT.set (this.vectorT.x / a, this.vectorT.y / this.vwr.getUnitCellInfo (1), this.vectorT.z / this.vwr.getUnitCellInfo (2));
} else {
this.vectorT.set (this.vectorT.x * this.tickInfo.scale.x, this.vectorT.y * this.tickInfo.scale.y, this.vectorT.z * this.tickInfo.scale.z);
}}var d = this.vectorT.length () + 0.0001 * dx;
if (d < dx) return;
var f = dx / d * d0 / d;
this.vectorT.scale (f);
var dz = (ptB.sZ - ptA.sZ) / (d / dx);
d += this.tickInfo.first;
var p = (Clazz.doubleToInt (Math.floor (this.tickInfo.first / dx))) * dx - this.tickInfo.first;
this.pointT.scaleAdd2 (p / dx, this.vectorT, ptA);
p += this.tickInfo.first;
var z = ptA.sZ;
if (diameter < 0) diameter = 1;
this.vectorT2.set (-this.vectorT2.y, this.vectorT2.x, 0);
this.vectorT2.scale (length / this.vectorT2.length ());
var ptRef = this.tickInfo.reference;
if (ptRef == null) {
this.pointT3.setT (this.vwr.getBoundBoxCenter ());
if (this.vwr.g.axesMode === J.c.AXES.BOUNDBOX) {
this.pointT3.add3 (1, 1, 1);
}} else {
this.pointT3.setT (ptRef);
}this.tm.transformPtScr (this.pointT3, this.pt2i);
var horizontal = (Math.abs (this.vectorT2.x / this.vectorT2.y) < 0.2);
var centerX = horizontal;
var centerY = !horizontal;
var rightJustify = !centerX && (this.vectorT2.x < 0);
var drawLabel = (formats != null && formats.length > 0);
var x;
var y;
var val =  new Array (1);
var i = (this.draw000 ? 0 : -1);
while (p < d) {
if (p >= this.tickInfo.first) {
this.pointT2.setT (this.pointT);
this.tm.transformPt3f (this.pointT2, this.pointT2);
this.drawLine (Clazz.doubleToInt (Math.floor (this.pointT2.x)), Clazz.doubleToInt (Math.floor (this.pointT2.y)), Clazz.floatToInt (z), (x = Clazz.doubleToInt (Math.floor (this.pointT2.x + this.vectorT2.x))), (y = Clazz.doubleToInt (Math.floor (this.pointT2.y + this.vectorT2.y))), Clazz.floatToInt (z), diameter);
if (drawLabel && (this.draw000 || p != 0)) {
val[0] = Float.$valueOf ((p == 0 ? 0 : p * signFactor));
var s = JU.PT.sprintf (formats[i % formats.length], "f", val);
this.drawString (x, y, Clazz.floatToInt (z), 4, rightJustify, centerX, centerY, Clazz.doubleToInt (Math.floor (this.pointT2.y)), s);
}}this.pointT.add (this.vectorT);
p += dx;
z += dz;
i++;
}
}, "JU.Point3fi,JU.Point3fi,~N,~N,~N,~A");
Clazz.defineMethod (c$, "drawLine", 
function (x1, y1, z1, x2, y2, z2, diameter) {
return this.drawLine2 (x1, y1, z1, x2, y2, z2, diameter);
}, "~N,~N,~N,~N,~N,~N,~N");
Clazz.defineMethod (c$, "drawLine2", 
function (x1, y1, z1, x2, y2, z2, diameter) {
this.pt0i.set (x1, y1, z1);
this.pt1i.set (x2, y2, z2);
if (this.dotsOrDashes) {
if (this.dashDots != null) this.drawDashed (x1, y1, z1, x2, y2, z2, this.dashDots);
} else {
if (diameter < 0) {
this.g3d.drawDashedLine (4, 2, this.pt0i, this.pt1i);
return 1;
}this.g3d.fillCylinder (2, diameter, this.pt0i, this.pt1i);
}return Clazz.doubleToInt ((diameter + 1) / 2);
}, "~N,~N,~N,~N,~N,~N,~N");
Clazz.defineMethod (c$, "drawString", 
function (x, y, z, radius, rightJustify, centerX, centerY, yRef, sVal) {
if (sVal == null) return;
var width = this.font3d.stringWidth (sVal);
var height = this.font3d.getAscent ();
var xT = x;
if (rightJustify) xT -= Clazz.doubleToInt (radius / 2) + 2 + width;
 else if (centerX) xT -= Clazz.doubleToInt (radius / 2) + 2 + Clazz.doubleToInt (width / 2);
 else xT += Clazz.doubleToInt (radius / 2) + 2;
var yT = y;
if (centerY) yT += Clazz.doubleToInt (height / 2);
 else if (yRef == 0 || yRef < y) yT += height;
 else yT -= Clazz.doubleToInt (radius / 2);
var zT = z - radius - 2;
if (zT < 1) zT = 1;
this.g3d.drawString (sVal, this.font3d, xT, yT, zT, zT, 0);
}, "~N,~N,~N,~N,~B,~B,~B,~N,~S");
Clazz.defineMethod (c$, "drawDashed", 
function (xA, yA, zA, xB, yB, zB, array) {
if (array == null || this.width < 0) return;
var f = array[0];
var dx = xB - xA;
var dy = yB - yA;
var dz = zB - zA;
var n = 0;
var isNdots = (array === J.render.FontLineShapeRenderer.ndots);
var isDots = (isNdots || array === J.render.FontLineShapeRenderer.sixdots);
if (isDots) {
var d2 = (dx * dx + dy * dy) / (this.width * this.width);
if (isNdots) {
f = (Math.sqrt (d2) / 1.5);
n = Clazz.floatToInt (f) + 3;
} else if (d2 < 8) {
array = J.render.FontLineShapeRenderer.twodots;
} else if (d2 < 32) {
array = J.render.FontLineShapeRenderer.fourdots;
}}var ptS = array[1];
var ptE = array[2];
var colixS = this.colixA;
var colixE = (ptE == 0 ? this.colixB : this.colixA);
if (n == 0) n = array.length;
for (var i = 0, pt = 3; pt < n; pt++) {
i = (isNdots ? i + 1 : array[pt]);
var xS = Clazz.doubleToInt (Math.floor (xA + dx * i / f));
var yS = Clazz.doubleToInt (Math.floor (yA + dy * i / f));
var zS = Clazz.doubleToInt (Math.floor (zA + dz * i / f));
if (isDots) {
this.s1.set (xS, yS, zS);
if (pt == ptS) this.g3d.setC (this.colixA);
 else if (pt == ptE) this.g3d.setC (this.colixB);
this.g3d.fillSphereI (this.width, this.s1);
continue;
}if (pt == ptS) colixS = this.colixB;
i = array[++pt];
if (pt == ptE) colixE = this.colixB;
var xE = Clazz.doubleToInt (Math.floor (xA + dx * i / f));
var yE = Clazz.doubleToInt (Math.floor (yA + dy * i / f));
var zE = Clazz.doubleToInt (Math.floor (zA + dz * i / f));
this.fillCylinder (colixS, colixE, 2, this.width, xS, yS, zS, xE, yE, zE);
}
}, "~N,~N,~N,~N,~N,~N,~A");
Clazz.defineMethod (c$, "fillCylinder", 
function (colixA, colixB, endcaps, diameter, xA, yA, zA, xB, yB, zB) {
if (this.asLineOnly) this.g3d.drawLine (colixA, colixB, xA, yA, zA, xB, yB, zB);
 else this.g3d.fillCylinderXYZ (colixA, colixB, endcaps, (!this.isExport || this.mad == 1 ? diameter : this.mad), xA, yA, zA, xB, yB, zB);
}, "~N,~N,~N,~N,~N,~N,~N,~N,~N,~N");
Clazz.defineStatics (c$,
"dashes", [12, 0, 0, 2, 5, 7, 10],
"hDashes", [10, 7, 6, 1, 3, 4, 6, 7, 9],
"ndots", [0, 3, 1000],
"sixdots", [12, 3, 6, 1, 3, 5, 7, 9, 11],
"fourdots", [13, 3, 5, 2, 5, 8, 11],
"twodots", [12, 3, 4, 3, 9]);
});
