import re

filepath = "d:/BANGJEJE.DEV/CMS/admin/src/case-studies.html"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

new_main = """        <main x-data="dashboardData()" x-init="init()" class="relative">
          <div class="p-4 mx-auto max-w-(--breakpoint-2xl) md:p-6 lg:p-10" x-data="{ searchQuery: '', statusFilter: 'all', categoryFilter: 'all', showDeleteModal: false, csToDelete: null }">
            <include src="./partials/page-header.html" />
            
            <div class="flex flex-col gap-6 mt-8">
              <!-- Filters & Search -->
              <div class="flex flex-col md:flex-row justify-between gap-4">
                <div class="flex items-center gap-4 w-full md:w-auto">
                  <div class="relative w-full md:w-64">
                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500">
                      <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    </span>
                    <input type="text" x-model="searchQuery" placeholder="Search case studies..." class="w-full rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 py-3 pl-12 pr-4 text-sm text-gray-800 dark:text-gray-200 outline-none focus:border-brand-500 dark:focus:border-brand-500 transition-colors" />
                  </div>
                  
                  <select x-model="statusFilter" class="rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 py-3 px-4 text-sm text-gray-800 dark:text-gray-200 outline-none focus:border-brand-500 dark:focus:border-brand-500">
                    <option value="all">All Status</option>
                    <option value="published">Published</option>
                    <option value="draft">Drafts</option>
                  </select>

                  <select x-model="categoryFilter" class="rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 py-3 px-4 text-sm text-gray-800 dark:text-gray-200 outline-none focus:border-brand-500 dark:focus:border-brand-500">
                    <option value="all">All Categories</option>
                    <option value="Branding">Branding</option>
                    <option value="E-commerce">E-commerce</option>
                    <option value="Enterprise">Enterprise</option>
                    <option value="SaaS">SaaS</option>
                    <option value="Mobile App">Mobile App</option>
                  </select>
                </div>
              </div>

              <!-- Table -->
              <div class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-theme-sm">
                <div class="overflow-x-auto">
                  <table class="w-full whitespace-nowrap text-left text-sm text-gray-600 dark:text-gray-400">
                    <thead class="bg-gray-50/50 dark:bg-gray-800/50 text-gray-800 dark:text-gray-200">
                      <tr>
                        <th class="px-6 py-4 font-semibold">Project Title</th>
                        <th class="px-6 py-4 font-semibold">Category / Industry</th>
                        <th class="px-6 py-4 font-semibold text-center">Order</th>
                        <th class="px-6 py-4 font-semibold">Status</th>
                        <th class="px-6 py-4 font-semibold">Date</th>
                        <th class="px-6 py-4 font-semibold text-right">Actions</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100 dark:divide-gray-800">
                      <template x-for="cs in filteredCaseStudies(searchQuery, statusFilter, categoryFilter)" :key="cs.id">
                        <tr class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                          <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                              <div x-show="cs.featuredImage" class="h-10 w-10 flex-shrink-0 overflow-hidden rounded-md border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800">
                                <img :src="cs.featuredImage" class="h-full w-full object-cover" />
                              </div>
                              <div x-show="!cs.featuredImage" class="flex h-10 w-10 items-center justify-center flex-shrink-0 overflow-hidden rounded-md border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800 text-gray-400">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                              </div>
                              <div>
                                <p class="font-medium text-black dark:text-white" x-text="cs.title"></p>
                                <p class="text-xs text-gray-500" x-text="cs.slug"></p>
                              </div>
                            </div>
                          </td>
                          <td class="px-6 py-4">
                            <span x-text="cs.category || '-'"></span>
                            <span class="mx-1 text-gray-400">•</span>
                            <span x-text="cs.industry || '-'" class="text-xs"></span>
                          </td>
                          <td class="px-6 py-4 text-center">
                            <span class="inline-flex items-center justify-center h-6 w-6 rounded bg-gray-100 dark:bg-gray-800 text-xs font-bold text-gray-600 dark:text-gray-300" x-text="cs.order || '-'"></span>
                          </td>
                          <td class="px-6 py-4">
                            <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
                                  :class="{
                                    'bg-success-50 text-success-600 dark:bg-success-500/10 dark:text-success-500': cs.status === 'published',
                                    'bg-warning-50 text-warning-600 dark:bg-warning-500/10 dark:text-warning-500': cs.status === 'draft'
                                  }"
                                  x-text="formatStatus(cs.status)">
                            </span>
                          </td>
                          <td class="px-6 py-4 text-sm" x-text="formatDate(cs.updatedAt)"></td>
                          <td class="px-6 py-4 text-right">
                            <div class="flex items-center justify-end gap-3">
                              <a :href="'case-study-edit.html?id=' + cs.id" class="text-gray-400 hover:text-brand-500 transition-colors" title="Edit">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                              </a>
                              <button @click="csToDelete = cs; showDeleteModal = true" class="text-gray-400 hover:text-error-500 transition-colors" title="Delete">
                                <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                              </button>
                            </div>
                          </td>
                        </tr>
                      </template>
                      
                      <!-- Empty State -->
                      <tr x-show="filteredCaseStudies(searchQuery, statusFilter, categoryFilter).length === 0">
                        <td colspan="6" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                          <p>No case studies found.</p>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Delete Confirmation Modal -->
            <div x-show="showDeleteModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0" style="display: none;">
              <div class="fixed inset-0 bg-black/50 transition-opacity" @click="showDeleteModal = false"></div>
              <div class="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-gray-900 p-8 text-left shadow-theme-xl transition-all border border-gray-100 dark:border-gray-800">
                <div class="flex items-center gap-4 mb-6">
                  <div class="flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-error-50 dark:bg-error-500/10 sm:h-10 sm:w-10">
                    <svg class="h-6 w-6 text-error-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
                  </div>
                  <h3 class="text-xl font-semibold text-black dark:text-white">Delete Case Study</h3>
                </div>
                <p class="text-gray-600 dark:text-gray-400 mb-8">Are you sure you want to delete <span class="font-bold text-black dark:text-white" x-text="csToDelete?.title"></span>? This action cannot be undone.</p>
                <div class="flex flex-col-reverse sm:flex-row gap-3 sm:justify-end">
                  <button @click="showDeleteModal = false; csToDelete = null" class="rounded-lg border border-gray-200 dark:border-gray-700 px-5 py-2.5 font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors w-full sm:w-auto">Cancel</button>
                  <button @click="if(csToDelete) { deleteCaseStudy(csToDelete.id); showDeleteModal = false; csToDelete = null; }" class="rounded-lg bg-error-500 px-5 py-2.5 font-medium text-white hover:bg-error-600 transition-colors w-full sm:w-auto">Delete Case Study</button>
                </div>
              </div>
            </div>

          </div>
        </main>"""

content = re.sub(r'<main>.*?</main>', new_main, content, flags=re.DOTALL)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated case-studies.html")
