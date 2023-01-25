# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "NX_BakeIndirectLightning",
    "author" : "Franck Demongin",
    "description" : "Render animation or frame with EEVEE and bake indirect lighting before each render",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 0),
    "location" : "Topbar, Render menu",
    "warning" : "",
    "category" : "Render"
}

import os
import bpy

class NXBIL_OT_render_animation(bpy.types.Operator):
    bl_idname = "nxbil.render_animation"
    bl_label = "Bake Indirect lighting and Render Animation"
    bl_description = "Bake indirect lighting and render animation"
    
    _frame = 0
    _timer = None
    _path = None
    _filepath = None
    _format_default = ('PNG', 'png')
    _formats = {
        'PNG': 'png',
        'JPEG': 'jpg',
        'BMP': 'bmp',
        'OPEN_EXR': 'exr',
        'TIFF': 'tiff',
        'WEBP': 'webp'
    }
    _ext = None
    _run = False

    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'BLENDER_EEVEE'

    def format_filepath(self, filepath):
        path, file = os.path.split(filepath)
        
        if not os.path.isdir(path):
            self.report({'WARNING'}, f"{filepath} is not a valid filepath")
            return {'CANCELLED'}
                
        file_name = ''
        if len(file) > 0:
            file_name, _ = os.path.splitext(file)
            if not file_name.endswith('_'):
                file_name += '_'  
                      
        return os.path.join(path, file_name)
    
    def execute(self, context):
        context.scene.frame_current = self._frame                 
        bpy.ops.scene.light_cache_bake()        
        self._filepath = f"{self._path}{self._frame:04d}.{self._ext}"
        context.scene.render.filepath = self._filepath            
        bpy.ops.render.render(write_still=True)
        self._frame += 1
        self._run = False
        
        return {'FINISHED'}
    
    def modal(self, context, event):     
        scene = context.scene
        frame_end = scene.frame_end
         
        if event.type == 'ESC':
            context.window_manager.event_timer_remove(self._timer)
            scene.render.filepath = self._path
            self.report({'WARNING'}, f"Exit {self._frame - 1}/{frame_end}")    
            
            return {'CANCELLED'}     

        if self._frame > frame_end: 
            context.window_manager.event_timer_remove(self._timer)
            scene.render.filepath = self._path
            self.report({'INFO'}, f"Finish {frame_end}/{frame_end}")    
            
            return {'FINISHED'}

        if event.type == 'TIMER':            
            if not self._run:
                self._run = True
                self.execute(context)
                areas = [area for area in context.screen.areas if area.type in ['VIEW_3D', 'IMAGE_EDITOR']]
                if len(areas) > 0:
                    area = areas[-1]
                    with context.temp_override(area=area):
                        context.area.type = 'IMAGE_EDITOR'
                        img = bpy.data.images.load(self._filepath, check_existing=False)
                        context.area.spaces.active.image = img                
           
        return {'PASS_THROUGH'}

    def invoke(self, context, _):   
        wm = context.window_manager        

        self._path = self.format_filepath(context.scene.render.filepath)
        
        format = context.scene.render.image_settings.file_format        
        if not format in self._formats.keys():
            context.scene.render.image_settings.file_format = self._format_default[0]
            self._ext = self._format_default[1]
        else:
            self._ext = self._formats[format]
        
        self._frame = context.scene.frame_start    
        
        self._timer = wm.event_timer_add(0.1, window=context.window)        
        wm.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


class NXBIL_OT_render_image(bpy.types.Operator):
    bl_idname = "nxbil.render_image"
    bl_label = "Bake indirect lighting and render image"
    bl_description = "Bake indirect lighting and render current frame"    
    
    @classmethod
    def poll(cls, context):
        return context.scene.render.engine == 'BLENDER_EEVEE'

    def execute(self, context):
        bpy.ops.scene.light_cache_bake()               
        bpy.ops.render.render('INVOKE_DEFAULT')
        
        return {'FINISHED'}


def nxbil_menu(self, context):
    self.layout.separator()
    self.layout.operator("nxbil.render_image", text="BIL and Render Image", icon="RENDER_STILL")
    self.layout.operator("nxbil.render_animation", text="BIL and Render Animation", icon="RENDER_ANIMATION")

classes = (
    NXBIL_OT_render_animation,
    NXBIL_OT_render_image,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_render.append(nxbil_menu)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Screen', space_type='EMPTY')
        kmi = km.keymap_items.new(NXBIL_OT_render_image.bl_idname, 
                type='F12', 
                value='PRESS', 
                alt=True)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(NXBIL_OT_render_animation.bl_idname, 
                type='F12', 
                value='PRESS', 
                shift=True, 
                alt=True)
        addon_keymaps.append((km, kmi))

def unregister():    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    bpy.types.TOPBAR_MT_render.remove(nxbil_menu)

    for cls in classes:
        bpy.utils.unregister_class(cls)

if '__main__' in __name__:
    register()
