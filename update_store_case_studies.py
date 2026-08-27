import re

filepath = "d:/BANGJEJE.DEV/CMS/admin/src/js/store.js"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Make sure we don't duplicate
if "createCaseStudy" not in content:
    # Inject Case Studies CRUD after deleteArticle
    crud_logic = """    deleteArticle(id) {
      const article = this.articles.find(a => a.id === id);
      if (!article) return false;

      this.articles = this.articles.filter(a => a.id !== id);
      this.logActivity('article_deleted', 'Deleted article "' + article.title + '"', 'article', id);
      this.saveToStorage();
      return true;
    },

    // Case Studies CRUD
    createCaseStudy(csData) {
      const now = new Date().toISOString();
      // Default order to length + 1 if not provided
      const order = csData.order || (this.caseStudies.length + 1);
      
      const newCS = {
        ...csData,
        id: this.generateId('cs'),
        order: order,
        createdAt: now,
        updatedAt: now,
        publishedAt: csData.status === 'published' ? now : null
      };
      
      this.caseStudies.push(newCS);
      this.logActivity(
        csData.status === 'published' ? 'case_study_published' : 'case_study_created',
        (csData.status === 'published' ? 'Published' : 'Drafted') + ' case study "' + newCS.title + '"',
        'caseStudy',
        newCS.id
      );
      this.saveToStorage();
      return newCS.id;
    },

    updateCaseStudy(id, csData) {
      const index = this.caseStudies.findIndex(a => a.id === id);
      if (index === -1) return null;

      const now = new Date().toISOString();
      const oldCS = this.caseStudies[index];
      
      let publishedAt = oldCS.publishedAt;
      let activityType = 'case_study_updated';
      let activityMessage = 'Updated case study "' + csData.title + '"';

      if (oldCS.status === 'draft' && csData.status === 'published') {
        publishedAt = oldCS.publishedAt || now;
        activityType = 'case_study_published';
        activityMessage = 'Published case study "' + csData.title + '"';
      } else if (oldCS.status === 'published' && csData.status === 'draft') {
        activityType = 'case_study_updated'; // Using updated as drafted isn't strictly requested for CS, but updated is fine. Or maybe case_study_updated
        activityMessage = 'Moved case study "' + csData.title + '" to drafts';
      }

      this.caseStudies[index] = {
        ...oldCS,
        ...csData,
        updatedAt: now,
        publishedAt
      };

      this.logActivity(activityType, activityMessage, 'caseStudy', id);
      this.saveToStorage();
      return id;
    },

    deleteCaseStudy(id) {
      const cs = this.caseStudies.find(a => a.id === id);
      if (!cs) return false;

      this.caseStudies = this.caseStudies.filter(a => a.id !== id);
      this.logActivity('case_study_deleted', 'Deleted case study "' + cs.title + '"', 'caseStudy', id);
      this.saveToStorage();
      return true;
    },"""
    
    content = re.sub(
        r'deleteArticle\(id\).*?return true;\s+}',
        crud_logic,
        content,
        flags=re.DOTALL
    )

    # We also need to add a filteredCaseStudies method for the list page
    list_logic = """    filteredArticles(searchQuery = '', statusFilter = 'all') {
      let filtered = this.articles;
      
      if (searchQuery) {
        const lowerSearch = searchQuery.toLowerCase();
        filtered = filtered.filter(a => 
          a.title.toLowerCase().includes(lowerSearch) || 
          a.excerpt.toLowerCase().includes(lowerSearch)
        );
      }

      if (statusFilter !== 'all') {
        filtered = filtered.filter(a => a.status === statusFilter);
      }

      return filtered.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
    },

    filteredCaseStudies(searchQuery = '', statusFilter = 'all', categoryFilter = 'all') {
      let filtered = this.caseStudies;
      
      if (searchQuery) {
        const lowerSearch = searchQuery.toLowerCase();
        filtered = filtered.filter(a => 
          a.title.toLowerCase().includes(lowerSearch) || 
          (a.description && a.description.toLowerCase().includes(lowerSearch))
        );
      }

      if (statusFilter !== 'all') {
        filtered = filtered.filter(a => a.status === statusFilter);
      }
      
      if (categoryFilter !== 'all') {
        filtered = filtered.filter(a => a.category === categoryFilter);
      }

      // Sort by order ASC, then updatedAt DESC
      return filtered.sort((a, b) => {
        if ((a.order || 0) !== (b.order || 0)) {
           return (a.order || 0) - (b.order || 0);
        }
        return new Date(b.updatedAt) - new Date(a.updatedAt);
      });
    }"""
    
    content = re.sub(
        r'filteredArticles\(searchQuery.*?\}.*?\}',
        list_logic,
        content,
        flags=re.DOTALL
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("store.js updated.")
else:
    print("Already updated.")
