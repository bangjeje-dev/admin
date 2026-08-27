export default function dashboardData() {
  const STORAGE_KEY = 'bangjeje_cms_data';

  return {
    articles: [
      {
        id: 'art-1',
        title: 'Understanding Modern Web Architecture',
        slug: 'understanding-modern-web-architecture',
        excerpt: 'A deep dive into frontend tooling and backend separation.',
        content: '<p>Content goes here...</p>',
        status: 'published',
        publishedAt: '2026-08-25T10:00:00Z',
        createdAt: '2026-08-24T08:00:00Z',
        updatedAt: '2026-08-25T10:05:00Z'
      },
      {
        id: 'art-2',
        title: 'The Future of AI in Content Management',
        slug: 'future-of-ai-cms',
        excerpt: 'How AI is reshaping content creation workflows.',
        content: '<p>Content goes here...</p>',
        status: 'draft',
        publishedAt: null,
        createdAt: '2026-08-26T09:00:00Z',
        updatedAt: '2026-08-26T09:30:00Z'
      },
      {
        id: 'art-3',
        title: 'Mastering Tailwind CSS for Enterprise',
        slug: 'mastering-tailwind-enterprise',
        excerpt: 'Scaling utility-first CSS in large codebases.',
        content: '<p>Content goes here...</p>',
        status: 'published',
        publishedAt: '2026-07-15T14:00:00Z',
        createdAt: '2026-07-10T11:00:00Z',
        updatedAt: '2026-07-15T14:00:00Z'
      }
    ],

    caseStudies: [
      {
        id: 'cs-1',
        title: 'E-commerce Migration to Headless CMS',
        slug: 'ecommerce-migration-headless',
        description: 'Increased performance by 40% after migration.',
        category: 'E-commerce',
        status: 'published',
        createdAt: '2026-08-10T09:00:00Z',
        updatedAt: '2026-08-15T10:00:00Z'
      },
      {
        id: 'cs-2',
        title: 'Fintech Startup Brand Refresh',
        slug: 'fintech-startup-brand-refresh',
        description: 'Complete overhaul of digital identity.',
        category: 'Branding',
        status: 'draft',
        createdAt: '2026-08-26T10:00:00Z',
        updatedAt: '2026-08-26T10:00:00Z'
      }
    ],

    digitalAssets: [
      {
        id: 'da-1',
        name: 'Brand Guidelines 2026',
        type: 'PDF',
        url: '/assets/brand-guidelines-2026.pdf',
        status: 'published',
        createdAt: '2026-08-01T10:00:00Z',
        updatedAt: '2026-08-01T10:00:00Z'
      },
      {
        id: 'da-2',
        name: 'Hero Image Fallback',
        type: 'Image',
        url: '/assets/hero-fallback.jpg',
        status: 'published',
        createdAt: '2026-08-20T14:30:00Z',
        updatedAt: '2026-08-20T14:30:00Z'
      },
      {
        id: 'da-3',
        name: 'Q3 Marketing Assets',
        type: 'ZIP',
        url: '/assets/q3-marketing.zip',
        status: 'draft',
        createdAt: '2026-08-25T11:00:00Z',
        updatedAt: '2026-08-26T09:00:00Z'
      }
    ],

    activities: [
      {
        id: 'act-1',
        type: 'article_published',
        message: 'Published article "Understanding Modern Web Architecture"',
        entityType: 'article',
        entityId: 'art-1',
        createdAt: '2026-08-25T10:00:00Z'
      },
      {
        id: 'act-2',
        type: 'asset_uploaded',
        message: 'Uploaded digital asset "Q3 Marketing Assets"',
        entityType: 'digitalAsset',
        entityId: 'da-3',
        createdAt: '2026-08-25T11:00:00Z'
      },
      {
        id: 'act-3',
        type: 'article_drafted',
        message: 'Drafted article "The Future of AI in Content Management"',
        entityType: 'article',
        entityId: 'art-2',
        createdAt: '2026-08-26T09:00:00Z'
      }
    ],

    adminUser: {
      id: 'usr-1',
      name: 'Musharof',
      email: 'admin@bangjeje.dev',
      avatar: './images/user/owner.jpg',
      role: 'admin'
    },

    // Initialization & Hydration
    init() {
      const storedData = localStorage.getItem(STORAGE_KEY);
      if (storedData) {
        const parsed = JSON.parse(storedData);
        this.articles = parsed.articles || this.articles;
        this.caseStudies = parsed.caseStudies || this.caseStudies;
        this.digitalAssets = parsed.digitalAssets || this.digitalAssets;
        this.activities = parsed.activities || this.activities;
      } else {
        this.saveToStorage();
      }
    },

    saveToStorage() {
      const dataToSave = {
        articles: this.articles,
        caseStudies: this.caseStudies,
        digitalAssets: this.digitalAssets,
        activities: this.activities
      };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(dataToSave));
    },

    generateId(prefix) {
      return prefix + '-' + Math.random().toString(36).substr(2, 9);
    },

    logActivity(type, message, entityType, entityId) {
      this.activities.unshift({
        id: this.generateId('act'),
        type,
        message,
        entityType,
        entityId,
        createdAt: new Date().toISOString()
      });
      this.saveToStorage();
    },

    // Articles CRUD
    createArticle(articleData) {
      const now = new Date().toISOString();
      const newArticle = {
        ...articleData,
        id: this.generateId('art'),
        createdAt: now,
        updatedAt: now,
        publishedAt: articleData.status === 'published' ? now : null
      };
      
      this.articles.unshift(newArticle);
      this.logActivity(
        articleData.status === 'published' ? 'article_published' : 'article_created',
        (articleData.status === 'published' ? 'Published' : 'Drafted') + ' article "' + newArticle.title + '"',
        'article',
        newArticle.id
      );
      this.saveToStorage();
      return newArticle.id;
    },

    updateArticle(id, articleData) {
      const index = this.articles.findIndex(a => a.id === id);
      if (index === -1) return null;

      const now = new Date().toISOString();
      const oldArticle = this.articles[index];
      
      // Determine if published status changed to Published
      let publishedAt = oldArticle.publishedAt;
      let activityType = 'article_updated';
      let activityMessage = 'Updated article "' + articleData.title + '"';

      if (oldArticle.status === 'draft' && articleData.status === 'published') {
        publishedAt = oldArticle.publishedAt || now;
        activityType = 'article_published';
        activityMessage = 'Published article "' + articleData.title + '"';
      } else if (oldArticle.status === 'published' && articleData.status === 'draft') {
        activityType = 'article_drafted';
        activityMessage = 'Moved article "' + articleData.title + '" to drafts';
      }

      this.articles[index] = {
        ...oldArticle,
        ...articleData,
        updatedAt: now,
        publishedAt
      };

      this.logActivity(activityType, activityMessage, 'article', id);
      this.saveToStorage();
      return id;
    },

        deleteArticle(id) {
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
    },

    // Digital Assets CRUD
    createDigitalAsset(daData) {
      const now = new Date().toISOString();
      // Default order to length + 1 if not provided
      const order = daData.order || (this.digitalAssets.length + 1);
      
      const newDA = {
        ...daData,
        id: this.generateId('da'),
        order: order,
        createdAt: now,
        updatedAt: now,
        publishedAt: daData.status === 'published' ? now : null
      };
      
      this.digitalAssets.push(newDA);
      this.logActivity(
        daData.status === 'published' ? 'asset_published' : 'asset_created',
        (daData.status === 'published' ? 'Published' : 'Drafted') + ' digital asset "' + newDA.title + '"',
        'digitalAsset',
        newDA.id
      );
      this.saveToStorage();
      return newDA.id;
    },

    updateDigitalAsset(id, daData) {
      const index = this.digitalAssets.findIndex(a => a.id === id);
      if (index === -1) return null;

      const now = new Date().toISOString();
      const oldDA = this.digitalAssets[index];
      
      let publishedAt = oldDA.publishedAt;
      let activityType = 'asset_updated';
      let activityMessage = 'Updated digital asset "' + daData.title + '"';

      if (oldDA.status === 'draft' && daData.status === 'published') {
        publishedAt = oldDA.publishedAt || now;
        activityType = 'asset_published';
        activityMessage = 'Published digital asset "' + daData.title + '"';
      } else if (oldDA.status === 'published' && daData.status === 'draft') {
        activityType = 'asset_updated';
        activityMessage = 'Moved digital asset "' + daData.title + '" to drafts';
      }

      this.digitalAssets[index] = {
        ...oldDA,
        ...daData,
        updatedAt: now,
        publishedAt
      };

      this.logActivity(activityType, activityMessage, 'digitalAsset', id);
      this.saveToStorage();
      return id;
    },

    deleteDigitalAsset(id) {
      const da = this.digitalAssets.find(a => a.id === id);
      if (!da) return false;

      this.digitalAssets = this.digitalAssets.filter(a => a.id !== id);
      this.logActivity('asset_deleted', 'Deleted digital asset "' + (da.title || da.name) + '"', 'digitalAsset', id);
      this.saveToStorage();
      return true;
    },

    // Format Date helper
    formatDate(dateString) {
      if (!dateString) return '-';
      const options = { year: 'numeric', month: 'short', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },

    // Status display helper
    formatStatus(status) {
      if (!status) return '';
      return status.charAt(0).toUpperCase() + status.slice(1);
    },

    // Computed properties / Getters
    get isThisMonth() {
      const now = new Date();
      const currentMonth = now.getMonth();
      const currentYear = now.getFullYear();
      return (dateString) => {
        const d = new Date(dateString);
        return d.getMonth() === currentMonth && d.getFullYear() === currentYear;
      };
    },

    get articlesCreatedThisMonth() {
      return this.articles.filter(a => this.isThisMonth(a.createdAt)).length;
    },

    get caseStudiesCreatedThisMonth() {
      return this.caseStudies.filter(c => this.isThisMonth(c.createdAt)).length;
    },

    get digitalAssetsCreatedThisMonth() {
      return this.digitalAssets.filter(d => this.isThisMonth(d.createdAt)).length;
    },

    get recentArticles() {
      return [...this.articles]
        .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
        .slice(0, 5);
    },

    get recentCaseStudies() {
      return [...this.caseStudies]
        .sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt))
        .slice(0, 5);
    },

    get recentActivities() {
      return [...this.activities]
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
        .slice(0, 5);
    },

        filteredArticles(searchQuery = '', statusFilter = 'all') {
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
    },

    filteredDigitalAssets(searchQuery = '', statusFilter = 'all', categoryFilter = 'all', typeFilter = 'all', pricingFilter = 'all') {
      let filtered = this.digitalAssets;
      
      if (searchQuery) {
        const lowerSearch = searchQuery.toLowerCase();
        filtered = filtered.filter(a => 
          (a.title && a.title.toLowerCase().includes(lowerSearch)) || 
          (a.name && a.name.toLowerCase().includes(lowerSearch)) ||
          (a.description && a.description.toLowerCase().includes(lowerSearch))
        );
      }

      if (statusFilter !== 'all') {
        filtered = filtered.filter(a => a.status === statusFilter);
      }
      
      if (categoryFilter !== 'all') {
        filtered = filtered.filter(a => a.category === categoryFilter);
      }

      if (typeFilter !== 'all') {
        filtered = filtered.filter(a => (a.type && a.type.toLowerCase() === typeFilter.toLowerCase()));
      }

      if (pricingFilter !== 'all') {
        filtered = filtered.filter(a => a.pricingModel === pricingFilter);
      }

      // Sort by order ASC, then updatedAt DESC
      return filtered.sort((a, b) => {
        if ((a.order || 0) !== (b.order || 0)) {
           return (a.order || 0) - (b.order || 0);
        }
        return new Date(b.updatedAt) - new Date(a.updatedAt);
      });
    }
  };
}

export function settingsData() {
  const SETTINGS_KEY = 'bangjeje_cms_settings';
  const DASHBOARD_KEY = 'bangjeje_cms_data'; // for import/export

  return {
    settings: {
      general: {
        siteName: "BANGJEJE.DEV",
        siteUrl: "https://bangjeje.dev",
        siteDescription: "",
        logo: null,
        favicon: null,
        adminEmail: ""
      },
      seo: {
        metaTitle: "",
        metaDescription: "",
        ogImage: null,
        searchConsoleVerification: ""
      },
      social: {
        instagram: "",
        linkedin: "",
        facebook: "",
        twitter: "",
        github: "",
        behance: "",
        dribbble: ""
      },
      contact: {
        email: "",
        whatsapp: "",
        location: ""
      },
      navigation: [
        { id: "nav-home", label: "Home", url: "/", active: true, order: 1 },
        { id: "nav-services", label: "Services", url: "/services.html", active: true, order: 2 },
        { id: "nav-case-studies", label: "Case Studies", url: "/case-studies.html", active: true, order: 3 },
        { id: "nav-articles", label: "Articles", url: "/articles.html", active: true, order: 4 },
        { id: "nav-digital-assets", label: "Digital Assets", url: "/digital-assets.html", active: true, order: 5 },
        { id: "nav-about", label: "About", url: "/about.html", active: true, order: 6 },
        { id: "nav-contact", label: "Contact", url: "/contact.html", active: true, order: 7 }
      ],
      storage: {
        provider: "cloudflare-r2",
        bucket: "my-asset",
        publicAssetUrl: "",
        status: "not-configured"
      }
    },
    
    activeTab: 'general',
    showToast: false,
    toastMessage: '',

    init() {
      const stored = localStorage.getItem(SETTINGS_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        // Deep merge to preserve structure and new defaults
        this.settings = { ...this.settings, ...parsed };
      } else {
        this.saveToStorage();
      }
    },

    saveToStorage() {
      localStorage.setItem(SETTINGS_KEY, JSON.stringify(this.settings));
    },

    saveSettings() {
      this.saveToStorage();
      this.showToastMessage('Settings saved successfully!');
    },

    showToastMessage(msg) {
      this.toastMessage = msg;
      this.showToast = true;
      setTimeout(() => this.showToast = false, 3000);
    },

    handleImageUpload(e, category, field) {
      const file = e.target.files[0];
      if (file) {
        const r = new FileReader();
        r.onload = (ev) => {
          this.settings[category][field] = ev.target.result;
        };
        r.readAsDataURL(file);
      }
      e.target.value = '';
    },

    removeImage(category, field) {
      this.settings[category][field] = null;
    },

    // Navigation CRUD
    addNavItem() {
      const newOrder = this.settings.navigation.length > 0 
        ? Math.max(...this.settings.navigation.map(n => n.order)) + 1 
        : 1;
      this.settings.navigation.push({
        id: 'nav-' + Date.now(),
        label: 'New Item',
        url: '#',
        active: true,
        order: newOrder
      });
    },

    removeNavItem(id) {
      this.settings.navigation = this.settings.navigation.filter(n => n.id !== id);
    },

    // System Data Handling
    exportData() {
      const settingsData = localStorage.getItem(SETTINGS_KEY);
      const dashboardData = localStorage.getItem(DASHBOARD_KEY);
      
      const exportObj = {
        settings: settingsData ? JSON.parse(settingsData) : this.settings,
        dashboard: dashboardData ? JSON.parse(dashboardData) : {}
      };

      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportObj, null, 2));
      const downloadAnchorNode = document.createElement('a');
      downloadAnchorNode.setAttribute("href", dataStr);
      downloadAnchorNode.setAttribute("download", "bangjeje_cms_export.json");
      document.body.appendChild(downloadAnchorNode);
      downloadAnchorNode.click();
      downloadAnchorNode.remove();
    },

    importData(e) {
      const file = e.target.files[0];
      if (!file) return;
      
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const imported = JSON.parse(event.target.result);
          if (imported.settings) {
            localStorage.setItem(SETTINGS_KEY, JSON.stringify(imported.settings));
            this.settings = imported.settings;
          }
          if (imported.dashboard) {
            localStorage.setItem(DASHBOARD_KEY, JSON.stringify(imported.dashboard));
          }
          this.showToastMessage('Data imported successfully! Reloading...');
          setTimeout(() => window.location.reload(), 1500);
        } catch (err) {
          alert("Invalid JSON file.");
        }
      };
      reader.readAsText(file);
      e.target.value = '';
    },

    resetData() {
      if (confirm('Are you sure you want to completely reset all CMS data to defaults? This cannot be undone.')) {
        localStorage.removeItem(SETTINGS_KEY);
        localStorage.removeItem(DASHBOARD_KEY);
        this.showToastMessage('Data reset successfully! Reloading...');
        setTimeout(() => window.location.reload(), 1500);
      }
    }
  };
}
