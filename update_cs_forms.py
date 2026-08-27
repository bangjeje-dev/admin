import re
import os

def generate_html(mode="create"):
    is_edit = mode == "edit"
    
    init_logic = ""
    if is_edit:
        init_logic = """
                 init();
                 const urlParams = new URLSearchParams(window.location.search);
                 const csId = urlParams.get('id');
                 const found = caseStudies.find(a => a.id === csId);
                 if (found) {
                   csData = JSON.parse(JSON.stringify({
                     ...found,
                     overview: found.overview || { content: '', responsibilities: [] },
                     challenge: found.challenge || { content: '', considerations: [], points: [] },
                     objectives: found.objectives || [],
                     process: found.process || [],
                     deliverables: found.deliverables || { description: '', artifacts: [], tools: [], gallery: [] },
                     reflection: found.reflection || { content: '' },
                     featuredImage: found.featuredImage || null
                   }));
                 } else {
                   window.location.href = 'case-studies.html';
                 }
                 setTimeout(() => initEditors(), 100);
        """
    else:
        init_logic = "setTimeout(() => initEditors(), 100);"

    save_call = "this.updateCaseStudy(this.csData.id, this.csData);" if is_edit else "this.createCaseStudy(this.csData);"
    toast_msg = "Case Study updated successfully." if is_edit else "Case Study created successfully."

    # HTML string
    html = f"""        <main x-data="dashboardData()" {'x-init="init()"' if not is_edit else ''} class="relative">
          <div class="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6 lg:p-10" 
               x-data="{{ 
                 csData: {{ 
                   {'id: "",' if is_edit else ''}
                   title: '', slug: '', description: '', category: '', industry: '', role: '', platform: '', timeline: '', order: '', status: 'draft', featuredImage: null,
                   overview: {{ content: '', responsibilities: [] }},
                   challenge: {{ content: '', considerations: [], points: [] }},
                   objectives: [],
                   process: [],
                   deliverables: {{ description: '', artifacts: [], tools: [], gallery: [] }},
                   reflection: {{ content: '' }}
                 }},
                 autoSlug: { 'false' if is_edit else 'true' },
                 showToast: false,
                 errors: {{}},
                 
                 // Temp inputs for tags
                 tempResp: '', tempCons: '', tempChalPoint: '', tempArtifact: '', tempTool: '',
                 
                 initEditors() {{
                   const config = {{ theme: 'snow', modules: {{ blotFormatter: {{}}, toolbar: [['bold', 'italic', 'underline'], [{{ 'header': 2 }}, {{ 'header': 3 }}], [{{ 'list': 'ordered'}}, {{ 'list': 'bullet' }}], ['blockquote', 'code-block'], ['link', 'image'], [{{ 'align': [] }}], ['clean']] }} }};
                   
                   ['overview', 'challenge', 'deliverables', 'reflection'].forEach(key => {{
                     const q = new Quill('#editor-' + key, config);
                     q.on('text-change', () => {{
                       const html = q.root.innerHTML;
                       if (key === 'overview') this.csData.overview.content = html === '<p><br></p>' ? '' : html;
                       if (key === 'challenge') this.csData.challenge.content = html === '<p><br></p>' ? '' : html;
                       if (key === 'deliverables') this.csData.deliverables.description = html === '<p><br></p>' ? '' : html;
                       if (key === 'reflection') this.csData.reflection.content = html === '<p><br></p>' ? '' : html;
                     }});
                     // hydrate
                     let c = '';
                     if (key === 'overview') c = this.csData.overview.content;
                     if (key === 'challenge') c = this.csData.challenge.content;
                     if (key === 'deliverables') c = this.csData.deliverables.description;
                     if (key === 'reflection') c = this.csData.reflection.content;
                     if (c) q.root.innerHTML = c;
                   }});
                 }},
                 
                 addTag(arr, tempVar) {{
                   const val = this[tempVar].trim();
                   if (val && !arr.includes(val)) arr.push(val);
                   this[tempVar] = '';
                 }},
                 removeTag(arr, val) {{
                   const idx = arr.indexOf(val);
                   if(idx > -1) arr.splice(idx, 1);
                 }},
                 
                 addObjective() {{ this.csData.objectives.push({{ id: 'obj-'+Date.now(), title: '', description: '' }}); }},
                 removeObjective(idx) {{ this.csData.objectives.splice(idx, 1); }},
                 
                 addProcess() {{ this.csData.process.push({{ id: 'proc-'+Date.now(), phase: '', title: '', description: '' }}); }},
                 removeProcess(idx) {{ this.csData.process.splice(idx, 1); }},

                 handleFeaturedImage(e) {{
                   const file = e.target.files[0];
                   if (file) {{
                     const r = new FileReader(); r.onload = (ev) => this.csData.featuredImage = ev.target.result; r.readAsDataURL(file);
                   }}
                 }},
                 
                 handleGallery(e) {{
                   const files = e.target.files;
                   for(let i=0; i<files.length; i++) {{
                     const r = new FileReader();
                     r.onload = (ev) => this.csData.deliverables.gallery.push(ev.target.result);
                     r.readAsDataURL(files[i]);
                   }}
                   e.target.value = '';
                 }},
                 removeGalleryImage(idx) {{ this.csData.deliverables.gallery.splice(idx, 1); }},

                 validate() {{
                   this.errors = {{}};
                   if (!this.csData.title.trim()) this.errors.title = 'Title is required';
                   if (!this.csData.slug.trim()) this.errors.slug = 'Slug is required';
                   if (!this.csData.category) this.errors.category = 'Category is required';
                   
                   if (Object.keys(this.errors).length > 0) {{
                     const el = document.getElementById('field-' + Object.keys(this.errors)[0]);
                     if (el) el.focus();
                     return false;
                   }}
                   return true;
                 }},
                 
                 save(status) {{
                   if (!this.validate()) return;
                   this.csData.status = status;
                   {save_call}
                   this.showToast = true;
                   setTimeout(() => window.location.href = 'case-studies.html', 1000);
                 }}
               }}"
               x-init="
                 $watch('csData.title', val => {{
                   if (autoSlug) {{
                     csData.slug = val.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '');
                     if (csData.slug) delete errors.slug;
                   }}
                   if (val) delete errors.title;
                 }});
                 {init_logic}
               ">
            <include src="./partials/page-header.html" />
            
            <div class="flex flex-col xl:flex-row gap-6 mt-8">
              
              <!-- Main Column -->
              <div class="flex-1 flex flex-col gap-8">
                
                <!-- 1. Basic Info -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">Basic Information</h3>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div class="md:col-span-2">
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Project Title <span class="text-error-500">*</span></label>
                      <input id="field-title" type="text" x-model="csData.title" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white" :class="{{'border-error-500': errors.title}}" />
                      <p x-show="errors.title" x-text="errors.title" class="mt-1 text-sm text-error-500"></p>
                    </div>
                    <div class="md:col-span-2">
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Slug <span class="text-error-500">*</span></label>
                      <input id="field-slug" type="text" x-model="csData.slug" @input="autoSlug = false" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white" :class="{{'border-error-500': errors.slug}}" />
                      <p x-show="errors.slug" x-text="errors.slug" class="mt-1 text-sm text-error-500"></p>
                    </div>
                    <div class="md:col-span-2">
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Short Description</label>
                      <textarea rows="2" x-model="csData.description" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white"></textarea>
                    </div>
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Industry</label>
                      <input type="text" x-model="csData.industry" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white" />
                    </div>
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Role</label>
                      <input type="text" x-model="csData.role" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white" />
                    </div>
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Platform</label>
                      <input type="text" x-model="csData.platform" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white" />
                    </div>
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Timeline</label>
                      <input type="text" x-model="csData.timeline" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white" />
                    </div>
                  </div>
                </div>

                <!-- 2. Project Overview -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">01. Project Overview</h3>
                  <div class="flex flex-col gap-5">
                    <div>
                      <div id="editor-overview" class="w-full rounded-b-lg border-x border-b border-gray-200 dark:border-gray-700 text-black dark:text-white h-48"></div>
                    </div>
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Responsibilities</label>
                      <div class="flex flex-wrap gap-2 mb-3" x-show="csData.overview.responsibilities.length > 0">
                        <template x-for="r in csData.overview.responsibilities" :key="r">
                          <span class="inline-flex items-center gap-1.5 rounded-full bg-gray-100 dark:bg-gray-800 px-3 py-1 text-sm font-medium text-gray-800 dark:text-gray-200">
                            <span x-text="r"></span>
                            <button @click="removeTag(csData.overview.responsibilities, r)" class="text-gray-500 hover:text-error-500"><svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
                          </span>
                        </template>
                      </div>
                      <input type="text" x-model="tempResp" @keydown.enter.prevent="addTag(csData.overview.responsibilities, 'tempResp')" placeholder="Add responsibility and press Enter" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-2 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white text-sm" />
                    </div>
                  </div>
                </div>

                <!-- 3. The Challenge -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">02. The Challenge</h3>
                  <div class="flex flex-col gap-5">
                    <div>
                      <div id="editor-challenge" class="w-full rounded-b-lg border-x border-b border-gray-200 dark:border-gray-700 text-black dark:text-white h-48"></div>
                    </div>
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Core Considerations</label>
                      <div class="flex flex-wrap gap-2 mb-3" x-show="csData.challenge.considerations.length > 0">
                        <template x-for="c in csData.challenge.considerations" :key="c">
                          <span class="inline-flex items-center gap-1.5 rounded-full bg-gray-100 dark:bg-gray-800 px-3 py-1 text-sm font-medium text-gray-800 dark:text-gray-200">
                            <span x-text="c"></span>
                            <button @click="removeTag(csData.challenge.considerations, c)" class="text-gray-500 hover:text-error-500"><svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
                          </span>
                        </template>
                      </div>
                      <input type="text" x-model="tempCons" @keydown.enter.prevent="addTag(csData.challenge.considerations, 'tempCons')" placeholder="Add consideration and press Enter" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-2 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white text-sm" />
                    </div>
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Challenge Points</label>
                      <div class="flex flex-col gap-2 mb-3" x-show="csData.challenge.points.length > 0">
                        <template x-for="p in csData.challenge.points" :key="p">
                          <div class="flex items-center gap-3 rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-3">
                            <span class="flex-1 text-sm text-gray-800 dark:text-gray-200" x-text="p"></span>
                            <button @click="removeTag(csData.challenge.points, p)" class="text-gray-500 hover:text-error-500"><svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
                          </div>
                        </template>
                      </div>
                      <input type="text" x-model="tempChalPoint" @keydown.enter.prevent="addTag(csData.challenge.points, 'tempChalPoint')" placeholder="Add point and press Enter" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-2 outline-none focus:border-brand-500 dark:focus:border-brand-500 text-black dark:text-white text-sm" />
                    </div>
                  </div>
                </div>

                <!-- 4. Objectives -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <div class="flex justify-between items-center mb-5">
                    <h3 class="text-lg font-bold text-black dark:text-white">03. Objectives</h3>
                    <button @click="addObjective()" class="text-sm font-medium text-brand-500 hover:text-brand-600">+ Add Objective</button>
                  </div>
                  <div class="flex flex-col gap-4">
                    <template x-for="(obj, index) in csData.objectives" :key="obj.id">
                      <div class="relative rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-4">
                        <button @click="removeObjective(index)" class="absolute top-4 right-4 text-gray-400 hover:text-error-500"><svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pr-10">
                          <div>
                            <label class="mb-1 block text-xs font-medium text-gray-500">Title</label>
                            <input type="text" x-model="obj.title" class="w-full rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none text-black dark:text-white" />
                          </div>
                          <div>
                            <label class="mb-1 block text-xs font-medium text-gray-500">Description</label>
                            <input type="text" x-model="obj.description" class="w-full rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none text-black dark:text-white" />
                          </div>
                        </div>
                      </div>
                    </template>
                    <div x-show="csData.objectives.length === 0" class="text-center py-6 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
                      <p class="text-sm text-gray-500">No objectives added yet.</p>
                    </div>
                  </div>
                </div>

                <!-- 5. Process -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <div class="flex justify-between items-center mb-5">
                    <h3 class="text-lg font-bold text-black dark:text-white">04. Process</h3>
                    <button @click="addProcess()" class="text-sm font-medium text-brand-500 hover:text-brand-600">+ Add Step</button>
                  </div>
                  <div class="flex flex-col gap-4">
                    <template x-for="(proc, index) in csData.process" :key="proc.id">
                      <div class="relative rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-4">
                        <button @click="removeProcess(index)" class="absolute top-4 right-4 text-gray-400 hover:text-error-500"><svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pr-10">
                          <div class="md:col-span-1">
                            <label class="mb-1 block text-xs font-medium text-gray-500">Phase (e.g. 01)</label>
                            <input type="text" x-model="proc.phase" class="w-full rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none text-black dark:text-white" />
                          </div>
                          <div class="md:col-span-2">
                            <label class="mb-1 block text-xs font-medium text-gray-500">Title</label>
                            <input type="text" x-model="proc.title" class="w-full rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none text-black dark:text-white" />
                          </div>
                          <div class="md:col-span-3">
                            <label class="mb-1 block text-xs font-medium text-gray-500">Description</label>
                            <textarea rows="2" x-model="proc.description" class="w-full rounded border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-3 py-2 text-sm outline-none text-black dark:text-white"></textarea>
                          </div>
                        </div>
                      </div>
                    </template>
                    <div x-show="csData.process.length === 0" class="text-center py-6 border border-dashed border-gray-300 dark:border-gray-700 rounded-lg">
                      <p class="text-sm text-gray-500">No process steps added yet.</p>
                    </div>
                  </div>
                </div>

                <!-- 6. Deliverables -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">05. Deliverables</h3>
                  <div class="flex flex-col gap-5">
                    <div>
                      <div id="editor-deliverables" class="w-full rounded-b-lg border-x border-b border-gray-200 dark:border-gray-700 text-black dark:text-white h-48"></div>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                      <div>
                        <label class="mb-2.5 block font-medium text-black dark:text-white">Project Artifacts</label>
                        <div class="flex flex-wrap gap-2 mb-3" x-show="csData.deliverables.artifacts.length > 0">
                          <template x-for="a in csData.deliverables.artifacts" :key="a">
                            <span class="inline-flex items-center gap-1.5 rounded-full bg-gray-100 dark:bg-gray-800 px-3 py-1 text-sm font-medium text-gray-800 dark:text-gray-200">
                              <span x-text="a"></span>
                              <button @click="removeTag(csData.deliverables.artifacts, a)" class="text-gray-500 hover:text-error-500"><svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
                            </span>
                          </template>
                        </div>
                        <input type="text" x-model="tempArtifact" @keydown.enter.prevent="addTag(csData.deliverables.artifacts, 'tempArtifact')" placeholder="Add artifact..." class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-2 outline-none text-black dark:text-white text-sm" />
                      </div>
                      <div>
                        <label class="mb-2.5 block font-medium text-black dark:text-white">Tools</label>
                        <div class="flex flex-wrap gap-2 mb-3" x-show="csData.deliverables.tools.length > 0">
                          <template x-for="t in csData.deliverables.tools" :key="t">
                            <span class="inline-flex items-center gap-1.5 rounded-full bg-gray-100 dark:bg-gray-800 px-3 py-1 text-sm font-medium text-gray-800 dark:text-gray-200">
                              <span x-text="t"></span>
                              <button @click="removeTag(csData.deliverables.tools, t)" class="text-gray-500 hover:text-error-500"><svg class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg></button>
                            </span>
                          </template>
                        </div>
                        <input type="text" x-model="tempTool" @keydown.enter.prevent="addTag(csData.deliverables.tools, 'tempTool')" placeholder="Add tool..." class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-2 outline-none text-black dark:text-white text-sm" />
                      </div>
                    </div>
                    
                    <div>
                      <label class="mb-2.5 block font-medium text-black dark:text-white">Project Gallery</label>
                      <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 mb-4" x-show="csData.deliverables.gallery.length > 0">
                        <template x-for="(img, idx) in csData.deliverables.gallery" :key="idx">
                          <div class="relative rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden group aspect-video">
                            <img :src="img" class="w-full h-full object-cover" />
                            <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                              <button @click="removeGalleryImage(idx)" class="rounded bg-error-500 p-2 text-white hover:bg-error-600"><svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg></button>
                            </div>
                          </div>
                        </template>
                      </div>
                      <div class="relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-6 text-center hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer" @click="document.getElementById('gallery-upload').click()">
                        <p class="text-sm font-medium text-black dark:text-white">Click to add images</p>
                        <p class="text-xs text-gray-500">Supports multiple files</p>
                      </div>
                      <input id="gallery-upload" type="file" multiple accept="image/*" class="hidden" @change="handleGallery" />
                    </div>
                  </div>
                </div>

                <!-- 7. Reflection -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">07. Reflection</h3>
                  <div>
                    <div id="editor-reflection" class="w-full rounded-b-lg border-x border-b border-gray-200 dark:border-gray-700 text-black dark:text-white h-48"></div>
                  </div>
                </div>

              </div>

              <!-- Sidebar Column -->
              <div class="w-full xl:w-1/3 flex flex-col gap-6">
                <!-- Publishing -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">Publishing</h3>
                  <div class="mb-4" x-show="csData.updatedAt">
                    <p class="text-sm text-gray-500 dark:text-gray-400">Current Status: <span class="font-medium text-black dark:text-white" x-text="formatStatus(csData.status)"></span></p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1" x-show="csData.publishedAt">Published on: <span x-text="formatDate(csData.publishedAt)"></span></p>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">Last updated: <span x-text="formatDate(csData.updatedAt)"></span></p>
                  </div>
                  <div class="flex flex-col gap-4">
                    <button @click="save('published')" class="flex w-full items-center justify-center rounded-lg bg-brand-500 px-5 py-3 font-medium text-white hover:bg-brand-600 transition-colors" x-text="csData.status === 'published' ? 'Update Case Study' : 'Publish Now'"></button>
                    <button @click="save('draft')" class="flex w-full items-center justify-center rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-5 py-3 font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800" x-show="csData.status !== 'draft'">Switch to Draft</button>
                    <button @click="save('draft')" class="flex w-full items-center justify-center rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 px-5 py-3 font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800" x-show="csData.status === 'draft'">Save Draft</button>
                  </div>
                </div>
                
                <!-- Category -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">Category <span class="text-error-500">*</span></h3>
                  <div>
                    <select id="field-category" x-model="csData.category" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none text-black dark:text-white" :class="{{'border-error-500': errors.category}}">
                      <option value="" disabled>Select category...</option>
                      <option value="Branding">Branding</option>
                      <option value="E-commerce">E-commerce</option>
                      <option value="Enterprise">Enterprise</option>
                      <option value="SaaS">SaaS</option>
                      <option value="Mobile App">Mobile App</option>
                    </select>
                    <p x-show="errors.category" x-text="errors.category" class="mt-1 text-sm text-error-500"></p>
                  </div>
                </div>

                <!-- Ordering -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">Global Order</h3>
                  <div>
                    <p class="text-xs text-gray-500 mb-2">Lower numbers appear first. Determines Next/Prev.</p>
                    <input type="number" x-model.number="csData.order" class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-transparent px-5 py-3 outline-none text-black dark:text-white" />
                  </div>
                </div>

                <!-- Featured Image -->
                <div class="rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 p-6 shadow-theme-sm">
                  <h3 class="mb-5 text-lg font-bold text-black dark:text-white">Featured Image</h3>
                  <div class="flex flex-col gap-4">
                    <div x-show="!csData.featuredImage" class="relative flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 p-10 text-center hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer" @click="document.getElementById('featured-upload').click()">
                      <p class="text-sm font-medium text-black dark:text-white">Upload image</p>
                    </div>
                    <div x-show="csData.featuredImage" class="relative overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 group" style="display: none;">
                      <img :src="csData.featuredImage" class="w-full h-auto max-h-64 object-cover" />
                      <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                        <button @click="document.getElementById('featured-upload').click()" class="rounded bg-white px-3 py-1.5 text-sm font-medium text-gray-900">Replace</button>
                        <button @click="csData.featuredImage = null; document.getElementById('featured-upload').value = ''" class="rounded bg-error-500 px-3 py-1.5 text-sm font-medium text-white">Remove</button>
                      </div>
                    </div>
                    <input id="featured-upload" type="file" accept="image/*" class="hidden" @change="handleFeaturedImage" />
                  </div>
                </div>

              </div>
              
            </div>

            <!-- Toast -->
            <div x-show="showToast" x-transition class="fixed bottom-10 right-10 z-[99999] flex w-full max-w-xs items-center gap-4 rounded-xl bg-white dark:bg-gray-900 px-5 py-4 shadow-theme-md border border-gray-100 dark:border-gray-800" style="display: none;">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-success-50 dark:bg-success-500/15 text-success-500">
                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
              </div>
              <div>
                <h4 class="font-medium text-black dark:text-white">Success</h4>
                <p class="text-sm text-gray-500 dark:text-gray-400" x-text="'{toast_msg}'"></p>
              </div>
            </div>

          </div>
        </main>"""

    return html

def process_file(mode, filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # ensure quill is added
    if "quill-blot-formatter" not in content:
        content = content.replace(
            '</head>',
            '  <link href="https://cdn.quilljs.com/1.3.6/quill.snow.css" rel="stylesheet">\n    <script src="https://cdn.quilljs.com/1.3.6/quill.js"></script>\n    <script src="https://cdn.jsdelivr.net/npm/quill-blot-formatter@1.0.5/dist/quill-blot-formatter.min.js"></script>\n  </head>'
        )

    new_main = generate_html(mode)
    content = re.sub(r'<main>.*?</main>', new_main, content, flags=re.DOTALL)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

process_file("create", "d:/BANGJEJE.DEV/CMS/admin/src/case-study-create.html")
process_file("edit", "d:/BANGJEJE.DEV/CMS/admin/src/case-study-edit.html")
print("Updated case-study-create.html and case-study-edit.html")
