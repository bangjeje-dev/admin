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
    }
  };
}
