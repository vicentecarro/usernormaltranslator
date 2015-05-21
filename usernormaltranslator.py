#license GPL v2
#by Vicente Carro Fernandez - vicentecarro@gmail.com

#v0.9.0
#added Auto smooth button
#added Draw split normals button
#added Normal Size value    
#Offset -reset applies only to the selected vertices.
#v0.9.1
#fixed Multiply mode
#added support for Normals2Verteccolor
#minor changes
#v0.9.2


import bpy
from mathutils import Vector
from mathutils import Color
from bpy_extras import view3d_utils



def apply_vector(vector,mode):
    """
    Sums/Multiply the given vector to the current mesh
    """
    #normalize the given vector, as v
    v=Vector(vector)
    #v.normalize()
    
    #get the data of the current object
    ob = bpy.context.object
    obdata = ob.data
    
    #mandatory stupid step, calculate normals split, in object mode
    bpy.ops.object.mode_set(mode="OBJECT")
    obdata.calc_normals_split()
    
    #prepare a list for all the normals. Une per "loop"(vertice-per-faace)    
    normals = [Vector()]*len(obdata.loops)
    
    #loop all the loops (subvertices) in the mesh    
    for loop in obdata.loops:
        #get the index of the associated vertex
        vertexindex = loop.vertex_index
        #if the vertex is selected, sum/multiply the given vector
        if obdata.vertices[vertexindex].select:
            #sums the vector to the current vector
            if mode == "ADD":
                normals[loop.index] = loop.normal + v
            #or multiply the normal by the vector 
            elif mode == "MULTIPLY":                
                print ("values: %s"% str(v))
                normals[loop.index] = Vector([float(x) * float(y) for x,y in zip(loop.normal,v)])                
                print ("original: %s new: %s"% (loop.normal, normals[loop.index]))
        else:
            normals[loop.index] = loop.normal
        #in any case normalize the result
        normals[loop.index].normalize()
        
    obdata.normals_split_custom_set(normals)
    bpy.ops.object.mode_set(mode="EDIT")     
    

def spherize(context):    
    print ("in spherize")
    
    #influence
    influence = context.scene['unt_spherifyratio']
    
    #gets the location of the center of the center object
    if context.scene.centerobject:
        center = bpy.data.objects[context.scene.centerobject].location
    else:
        center = bpy.context.scene.cursor_location
    
    #get world matrix for the object
    worldmatrix = bpy.context.object.matrix_world
    
    ob = bpy.context.object
    obdata = ob.data
    
    #mandatory stupid step, calculate normals split, in object mode
    bpy.ops.object.mode_set(mode="OBJECT")
    
    obdata.calc_normals_split()
    
    #prepare a list for all the normals. One per "loop"(vertice-per-faace)    
    normals = [Vector()]*len(obdata.loops)
    
    #loop all the loops (subvertices) in the mesh
    for loop in obdata.loops:
        #obdata.calc_normals_split()
        vertexindex = loop.vertex_index            

        normals[loop.index] = loop.normal
        print ("normal: %s"% normals[loop.index])
        
        #if the vertex is selected, normalize the normal            
        if obdata.vertices[vertexindex].select:
            #get local coordinate of the related vertex
            localco = obdata.vertices[vertexindex].co
            #calculate the globla coordinates of the vertex
            globalco = worldmatrix * obdata.vertices[vertexindex].co
            #delta betwen the global location of the vertex and the center of the center object
            v= Vector([y-x for x,y in zip(globalco,center)])
            v.negate()
            v.normalize()                             
            #resulting vector (v*influence + normal*(1-influence))
            normals[loop.index] = v * float(influence) + normals[loop.index] * (float(1)-float(influence))
            #normals[loop.index].negate()
            normals[loop.index].normalize()
            print ("new normal: %s"% normals[loop.index])
            
    obdata.normals_split_custom_set(normals)
    bpy.ops.object.mode_set(mode="EDIT")   



class OP_vertexcolor2normals(bpy.types.Operator):
    """Vertex color to normals"""
    bl_idname = "object.vertexcolor2normals"
    bl_label = "VertexColor to Normals"
    
    def execute(self,context):
        print ("do stuff")
        return {'FINISHED'}

class OP_normal2vertexcolor(bpy.types.Operator):
    """Normals to vertex color"""
    bl_idname = "object.normals2vertexcolor"
    bl_label = "Normals to VertexColor"
    
    def execute(self,context):
        print ("normals to vertex colors")
        ob = bpy.context.object
        obdata = ob.data
        
        #mandatory stupid step, calculate normals split, in object mode
        bpy.ops.object.mode_set(mode="OBJECT")        
        obdata.calc_normals_split()  
        
        #loop all the loops (subvertices) in the mesh
        for loop in obdata.loops:
            #obdata.calc_normals_split()
            vertexindex = loop.vertex_index
            #if the vertex is selected, normalize the normal            
            if obdata.vertices[vertexindex].select:            
                print ("Vertex: %s"% vertexindex)
                #convert components into color
                print ("   Vector %s"% loop.normal)
                color = Color(loop.normal)
                print ("   Color: %s"%color)
                ob.data.vertex_colors[0].data[loop.index].color = loop.normal                
        bpy.ops.object.mode_set(mode="EDIT")   
        
        return {'FINISHED'}

class OP_remake_normalize(bpy.types.Operator):
    """Remake UserNormals"""
    bl_idname = "object.remake_normalize"
    bl_label = "Remake"
    
    def execute(self,context):
        print ("do stuff")
        return {'FINISHED'}

class OP_smooth_normalize(bpy.types.Operator):
    """Smooth normals"""
    bl_idname = "object.smooth_normalize"
    bl_label = "Smooth"
    
    def execute(self,context):
        print ("do stuff")
        return {'FINISHED'}

class OP_invert_normalize(bpy.types.Operator):
    """Invert normals"""
    bl_idname = "object.invert_normalize"
    bl_label = "Invert"
    
    def execute(self,context):
        print ("invert normals")
        #get the data of the current object
        ob = bpy.context.object
        obdata = ob.data
        
        #mandatory stupid step, calculate normals split, in object mode
        bpy.ops.object.mode_set(mode="OBJECT")
        
        obdata.calc_normals_split()
        
        #prepare a list for all the normals. Une per "loop"(vertice-per-faace)    
        normals = [Vector()]*len(obdata.loops)
        
        #loop all the loops (subvertices) in the mesh
        for loop in obdata.loops:
            #obdata.calc_normals_split()
            vertexindex = loop.vertex_index            

            normals[loop.index] = loop.normal
            print ("normal: %s"% normals[loop.index])
            
            #if the vertex is selected, normalize the normal            
            if obdata.vertices[vertexindex].select:
                
                normals[loop.index].negate()
                print ("normal negated: %s"% normals[loop.index])
                
        obdata.normals_split_custom_set(normals)
        bpy.ops.object.mode_set(mode="EDIT")     

        return {'FINISHED'}

class OP_normalize(bpy.types.Operator):
    """Normalize normals"""
    bl_idname = "object.normalize_normalize"
    bl_label = "Normalize"
    
    def execute(self,context):
        print ("normalize vertices")  
        
        #get the data of the current object
        ob = bpy.context.object
        obdata = ob.data
        
        #mandatory stupid step, calculate normals split, in object mode
        bpy.ops.object.mode_set(mode="OBJECT")
        obdata.calc_normals_split()
        
        #loop all the loops (subvertices) in the mesh    
        for loop in obdata.loops:
            #obdata.calc_normals_split()
            vertexindex = loop.vertex_index
            #if the vertex is selected, normalize the normal
            if obdata.vertices[vertexindex].select: 
                loop.normal.normalize()                        

        bpy.ops.object.mode_set(mode="EDIT")    

        return {'FINISHED'}

class OP_create_center_spherize(bpy.types.Operator):
    """Create empty for the center"""
    bl_idname = "object.create_center_spherize"
    bl_label = "Create center"
    
    def execute(self,context):
        print ("create empty for center")
        
        bpy.ops.object.mode_set(mode="OBJECT")  
        
        original = context.object
        
        bpy.ops.object.empty_add()
        name = bpy.context.active_object.name        
        
        #bpy.data.objects[name].select = False
        #bpy.context.active_object.select = False
        context.scene.objects.active=None
        
        
        #set the new empty as the center of spherize
        context.scene.centerobject = name
        
        bpy.ops.object.select_pattern(extend = False, pattern = original.name)
        context.scene.objects.active = original
        
        bpy.ops.object.mode_set(mode="EDIT")  
        return {'FINISHED'}

class OP_apply(bpy.types.Operator):
    """Apply the values in the normals.
    Support Offset and Spherize modes"""
    bl_idname = "object.apply"
    bl_label = "Apply"
    
    area = bpy.props.StringProperty()
    
    
        
    
    def execute(self,context):
        print ("do stuff")
        if self.area == "offset":            
            apply_vector((context.scene.unt_offsetx,context.scene.unt_offsety, context.scene.unt_offsetz), context.scene.unt_offsetmode )
        if self.area == "spherize":
            print ("Applying spherize")
            spherize(context)
            pass
        
        return {'FINISHED'}

class OP_reset(bpy.types.Operator):
    """Reset"""
    bl_idname = "object.reset"
    bl_label = "Reset"
    
    area = bpy.props.StringProperty()
    
    def execute(self,context):
        #just a test. It worked.
        #bpy.types.Object.unt_offsetx = bpy.props.FloatProperty( name="",description="", min=-10, max=10, default = 0)
        print ("reset normals on vertices")
        #store the curent normals
        #get the data of the current object
        ob = bpy.context.object
        obdata = ob.data
        
        #mandatory stupid step, calculate normals split, in object mode
        bpy.ops.object.mode_set(mode="OBJECT")        
        obdata.calc_normals_split()
        
        #original normals
        original_normals = [Vector()]*len(obdata.loops)

        #new normals
        normals = [Vector()]*len(obdata.loops)
        
        for loop in obdata.loops:
            original_normals[loop.index] = Vector(loop.normal)
            
        #clear the custom normal data
        bpy.ops.mesh.customdata_custom_splitnormals_clear()
        
        #init again the custom normal data, reseted
        bpy.ops.mesh.customdata_custom_splitnormals_add()
        #is required to recalculate the normals so they can be read below
        obdata.calc_normals_split()
        
        #loop all the loops (subvertices) in the mesh
        for loop in obdata.loops:
            
            #get the vertex associated to the loop
            vertexindex = loop.vertex_index
            
            #if the vertex is selected, normalize the normal
            if obdata.vertices[vertexindex].select:
                normals[loop.index] = loop.normal
            else:
                normals[loop.index] = original_normals[loop.index]
                
        obdata.normals_split_custom_set(normals)
        bpy.ops.object.mode_set(mode="EDIT")     

        return {'FINISHED'}

class OP_axis_button(bpy.types.Operator):
    """Apply offset to this axis"""
    bl_idname = "object.axis_button"
    bl_label = "Axis"
        
    axis = bpy.props.StringProperty()
    
    def execute(self,context):                
        print ("do stuff")
        idle = 0 if context.scene.unt_offsetmode == "ADD" else 1
        if self.axis == "x":
            value = context.scene.unt_offsetx
            apply_vector((value,idle,idle),context.scene.unt_offsetmode)
        if self.axis == "y":
            value = context.scene.unt_offsety
            apply_vector((idle,value,idle),context.scene.unt_offsetmode)
        if self.axis == "z":
            value = context.scene.unt_offsetz
            apply_vector((idle,idle,value),context.scene.unt_offsetmode)
            
        
        return {'FINISHED'}


class OP_numeric_button(bpy.types.Operator):    
    """Tooltip"""
    bl_idname = "object.process_value"
    bl_label = "Do process value"
    
    value = bpy.props.FloatProperty()
    axis = bpy.props.StringProperty()

    def execute(self, context):
        #bpy.ops.object.select_all(action='DESELECT')
        mode = context.scene.unt_offsetmode
        #OFFSET MODE (BOTH ADD AND MULTIPLY)
        if self.axis == "x":
            context.scene.unt_offsetx = self.value
            apply_vector((self.value,0,0) if mode == "ADD" else (self.value,1,1), context.scene.unt_offsetmode)
        if self.axis == "y":
            context.scene.unt_offsety = self.value
            apply_vector((0,self.value,0) if mode == "ADD" else (1,self.value,1), context.scene.unt_offsetmode)
        if self.axis == "z":
            context.scene.unt_offsetz = self.value
            apply_vector((0,0,self.value) if mode == "ADD" else (1,1,self.value), context.scene.unt_offsetmode)
            
        #SPHERIZE MODE
        if self.axis == "sr":
            context.scene.unt_spherifyratio = self.value
            spherize(context)
            
        return {'FINISHED'}

class UserNormalTranslatorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    #bl_idname = "SCENE_PT_layout"
    bl_idname = "OBJECT_PT_panel"
    bl_description = "Modify the normals of the selected vertices of the current object."
    bl_label = "User Normal Editor"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "mesh_edit"
    
   
    def draw_header(self, context):
        #apparently not neeeded
        #self.layout.label("User Normal Editor",icon='TRIA_RIGHT')
        pass


    def draw(self, context):
        layout = self.layout
        scene = context.scene        
        ob = context.object
        #offset mode
        box = layout.box()
        box.label("Offset")                
        row1 = box.row()
        row1.label("Mode:   ")
        row1.prop(scene, "unt_offsetmode", expand=True)
        row1.separator()
        row1.label("                                  ")
        row = box.row()       
        #X axis
        row2 = box.row()
        xbutton = row2.operator("object.axis_button","X")
        xbutton.axis = "x"
        row2.prop(scene, "unt_offsetx")       
        #nb stands for numeric buton        
        nb1 = row2.operator("object.process_value","-0.5")
        nb1.value = -0.5
        nb1.axis = "x"
        nb2 = row2.operator("object.process_value","-0.1")
        nb2.value = -0.1
        nb2.axis = "x"
        nb3 = row2.operator("object.process_value","+0.1")
        nb3.value = 0.1
        nb3.axis = "x"
        nb4 = row2.operator("object.process_value","+0.5")
        nb4.value = 0.5
        nb4.axis = "x"
        
        #Y axis
        row3 = box.row()
        ybutton = row3.operator("object.axis_button","Y")
        ybutton.axis = "y"
        row3.prop(scene, "unt_offsety")       
        #nb stands for numeric buton        
        nb1 = row3.operator("object.process_value","-0.5")
        nb1.value = -0.5
        nb1.axis = "y"
        nb2 = row3.operator("object.process_value","-0.1")
        nb2.value = -0.1
        nb2.axis = "y"
        nb3 = row3.operator("object.process_value","+0.1")
        nb3.value = 0.1
        nb3.axis = "y"
        nb4 = row3.operator("object.process_value","+0.5")
        nb4.value = 0.5
        nb4.axis = "y"
        
        
        row4 = box.row()
        zbutton = row4.operator("object.axis_button","Z")
        zbutton.axis = "z"
        row4.prop(scene, "unt_offsetz")       
        #nb stands for numeric buton        
        nb1 = row4.operator("object.process_value","-0.5")
        nb1.value = -0.5
        nb1.axis = "z"
        nb2 = row4.operator("object.process_value","-0.1")
        nb2.value = -0.1
        nb2.axis = "z"
        nb3 = row4.operator("object.process_value","+0.1")
        nb3.value = 0.1
        nb3.axis = "z"
        nb4 = row4.operator("object.process_value","+0.5")
        nb4.value = 0.5
        nb4.axis = "z"
        
        row5 = box.row()
        breset = row5.operator("object.reset")
        breset.area = "offset"
        row5.separator()
        row5.prop(scene,"unt_abs_value")        
        row5.prop(scene, "unt_world_space")
        
        row6 = box.row()
        row6.separator()
        bapply_of = row6.operator("object.apply")
        bapply_of.area = "offset"
        
        
        #spherify mode
        box = layout.box()
        box.label("Spherize")
        row = box.row()
        row.label("Ratio:")
        row.prop(scene, "unt_spherifyratio")
        nb1 = row.operator("object.process_value","0.1")
        nb1.value = 0.1
        nb1.axis = "sr"
        nb2 = row.operator("object.process_value","0.25")
        nb2.value = 0.25
        nb2.axis = "sr"
        nb3 = row.operator("object.process_value","0.5")
        nb3.value = 0.5
        nb3.axis = "sr"
        nb4 = row.operator("object.process_value","0.75")
        nb4.value = 0.75
        nb4.axis = "sr"
        nb5 = row.operator("object.process_value","1.0")
        nb5.value = float(1)
        nb5.axis = "sr"
        row = box.row()
        row.operator("object.create_center_spherize")     
        row.prop_search(scene, "centerobject", bpy.data, "objects", text="")           
        row.separator()
        bapply_sp = row.operator("object.apply")
        bapply_sp.area = "spherize"
        
        
        
        #normal editing tools
        box = layout.box()
        box.label("Normal Editing Tools")
        row = box.row()
        row.prop( context.object.data, "use_auto_smooth")
        row.separator()
        row.prop( context.object.data, "show_normal_loop")
        row.prop( context.scene.tool_settings, "normal_size")
        row = box.row()
        row.operator("object.normalize_normalize")
        row.operator("object.invert_normalize")
        breset = row.operator("object.reset")
        breset.area = "normal"
        row = box.row()
        row.operator("object.smooth_normalize")
        row.operator("object.remake_normalize")
        
        #edit values
        box = layout.box()
        box.label("Edit values (using Vertex colours)")
        row = box.row()
        row.operator("object.normals2vertexcolor")
        row.operator("object.vertexcolor2normals")

              
        box.separator()

        

def register():
    bpy.utils.register_module(__name__)
    #offset mode
    bpy.types.Scene.unt_offsetmode = bpy.props.EnumProperty(
        items=(
            ('ADD', "Add", ""),
            ('MULTIPLY', "Multiply", "")
        ),
        default='ADD'
    )
    #offset X
    bpy.types.Scene.unt_offsetx = bpy.props.FloatProperty( name="",description="", min=-2, max=2, default = 0)
    #offset Y
    bpy.types.Scene.unt_offsety = bpy.props.FloatProperty( name="",description="", min=-2, max=2, default = 0)
    #offset Z
    bpy.types.Scene.unt_offsetz = bpy.props.FloatProperty( name="",description="", min=-2, max=2, default = 0)
    #spherify ratio
    bpy.types.Scene.unt_spherifyratio = bpy.props.FloatProperty( name="",description="ratio of spherify", min=0, max=1, default = 0)
    #absolute value
    bpy.types.Scene.unt_abs_value = bpy.props.BoolProperty( name="Absolute value", default = False)
    #world space
    bpy.types.Scene.unt_world_space = bpy.props.BoolProperty( name="World space", default = False)
    bpy.types.Scene.centerobject = bpy.props.StringProperty(name="Center object", description="This object center will define the direction of the spherized normals")


    
    
def unregister():
    bpy.utils.unregister_module(__name__)
    #del bpy.types.Object.my_enum
    


if __name__ == "__main__":
    register()
