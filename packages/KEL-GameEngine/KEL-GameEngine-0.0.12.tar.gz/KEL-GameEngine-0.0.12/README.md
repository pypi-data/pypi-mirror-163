# Introduction
NOTE: This is under development and does not have many features.

This is a python Framework called KEL (Kinda Exploited Game Engine). Its build on top of pygame, thefore the name. In the future you might be able to call it a game engine but right now Its a tool i guess.
It (by the moment) does not have a UI and not many features. Of course u can excpect a lot of features in the future.

Anyway here is a code example of how u can use this. This is only in one file but it can of course be
in many files.

    from KEL import *

    class MoveCompPoly:
        def start(self):
            self.holdxPos = False
            self.holdxNeg = False
            self.holdyPos = False
            self.holdyNeg = False

            self.vX = 0
            self.vY = 0

            self.transformComp = KEL.getComponent('TransformPolyComp')
            self.collideComp = KEL.getComponent('CollidePolyComp')
            self.obj = KEL.getObject()

        def update(self):
            if KEL.Input('K_d', 'Down'): self.holdxPos = True # Using velocity
            if KEL.Input('K_d', 'Up'): self.holdxPos = False # Using velocity

            if KEL.Input('K_a', 'Down'): self.holdxNeg = True
            if KEL.Input('K_a', 'Up'): self.holdxNeg = False 

            if KEL.Input('K_w', 'Down'): self.holdyNeg = True
            if KEL.Input('K_w', 'Up'): self.holdyNeg = False

            if KEL.Input('K_s', 'Down'): self.holdyPos = True
            if KEL.Input('K_s', 'Up'): self.holdyPos = False


            if self.holdxPos: self.vX = 100
            elif self.vX > 0: self.vX = 0

            if self.holdxNeg: self.vX = -100
            elif self.vX < 0: self.vX = 0

            if self.holdyPos: self.vY = 100
            elif self.vY > 0: self.vY = 0

            if self.holdyNeg: self.vY = -100
            elif self.vY < 0: self.vY = 0

            self.transformComp.moveX(self.vX * KEL.deltaTime)
            self.transformComp.moveY(self.vY * KEL.deltaTime)


            if self.collideComp.collide:
                self.obj.material = "#ffffff"
            else:
                self.obj.material = "#d65d0e"


    # Creating Objects
    rect1Comps = [ RenderPolyComp(), TransformPolyComp([[100, 100], [200, 150], [300, 300], [200, 300]]), MoveCompPoly(), CollidePolyComp() ]
    rect2Comps = [ RenderPolyComp(), TransformPolyComp([[600, 600], [600, 710], [500, 500], [500, 400]])] 
    rect3Comps = [ RenderPolyComp(), TransformPolyComp( [[100, 100], [100, 200], [150, 250], [200, 200], [200, 100]] ) ]

    KEL.addObject(objectName='Poly1', components=rect1Comps) # There are some additional settings such as what models u should use (emptyModel is only available) or where to place the object (in the future with folders YAY)
    KEL.addObject(objectName='Poly2', components=rect2Comps)
    KEL.addObject(objectName='Poly3', hitbox=False, components=rect3Comps)


    # Create Materials
    KEL.createMaterial(materialName='Player', materialColor='#d65d0e')

    KEL.createMaterial(materialName='rectNoHitbox', materialColor='#123123')
    KEL.createMaterial(materialName='rectHitbox', materialColor='#987654')



    # Adding Materials
    KEL.addMaterial(materialName='Player', objectName='Poly1')
    KEL.addMaterial(materialName='rectHitbox', objectName='Poly2')
    KEL.addMaterial(materialName='rectNoHitbox', objectName='Poly3')
    KEL.coreModules['Screen'].color = "#282828"


    run()
    

Its a suprise what this does
This code does display all of the current features but this is a very simple example and u can go a lot longer.

# Explaining the code (and more)
Too understand whats going on u can do two things. Use ur brain and see what the functions do and look at the documentation.md.


# Download
The procces to download this is quit simple. Just use pip.
Pip command:
pip install KEL-GameEngine                              (If u know what ur doing u can ofc use pip3)

U can also visit the page on pypi here:
https://pypi.org/project/KEL-GameEngine/


# Patron
u thought
