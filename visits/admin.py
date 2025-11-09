from django.contrib import admin
from django.db.models import Count, Q
from django.urls import path
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from .models import Visit, UniqueVisitor

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'get_user_identifier', 
        'path', 
        'timestamp', 
        'ip_address',
        'is_authenticated'
    )
    
    # Fields to use for filtering in the sidebar
    list_filter = ('timestamp', 'user', 'path')
    
    # Fields to search across
    search_fields = ('user__username', 'session_key', 'path', 'ip_address')
    
    # Date hierarchy for quick navigation by day/month/year
    date_hierarchy = 'timestamp'
    
    # Mark anonymous visits clearly
    def get_user_identifier(self, obj):
        return obj.get_user_identifier()
    get_user_identifier.short_description = 'Visitor'

    def is_authenticated(self, obj):
        return bool(obj.user)
    is_authenticated.boolean = True
    is_authenticated.short_description = 'Logged In'

    # Read-only fields in the detail view
    readonly_fields = ('user', 'session_key', 'path', 'timestamp', 'user_agent', 'ip_address')
    
    # Disable "Add" and "Delete" actions to prevent manual data manipulation
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(UniqueVisitor)
class UniqueVisitorAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'first_visit', 'last_visit')
    list_filter = ('first_visit', 'last_visit')
    search_fields = ('user__username', 'ip_address')
    date_hierarchy = 'last_visit'
    readonly_fields = ('user', 'ip_address', 'first_visit', 'last_visit')
    
    def has_add_permission(self, request):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False


# --- Custom Admin View for Analytics Dashboard ---

class AnalyticsAdmin(admin.AdminSite):
    site_header = "Website Analytics Dashboard"
    site_title = "Custom Analytics"
    index_title = "Monitor Website Traffic"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('traffic-stats/', self.admin_view(self.traffic_stats_view), name='traffic_stats'),
        ]
        return custom_urls + urls

    def traffic_stats_view(self, request):
        
        # 1. Define timeframes
        now_dt = now()
        yesterday = now_dt - timedelta(days=1)
        last_7_days = now_dt - timedelta(days=7)
        last_30_days = now_dt - timedelta(days=30)
        
        # 2. Total Counts (Unique Visitors vs Total Visits)
        total_visits = Visit.objects.count()
        total_unique_visitors = UniqueVisitor.objects.count()
        
        # 3. Time-based Aggregations
        data = {
            'today': {'visits': 0, 'unique': 0, 'auth': 0, 'anon': 0},
            'last_7_days': {'visits': 0, 'unique': 0, 'auth': 0, 'anon': 0},
            'last_30_days': {'visits': 0, 'unique': 0, 'auth': 0, 'anon': 0},
        }

        # Calculate today's visits
        today_visits = Visit.objects.filter(timestamp__gte=yesterday)
        data['today']['visits'] = today_visits.count()
        data['today']['auth'] = today_visits.filter(user__isnull=False).count()
        data['today']['anon'] = today_visits.filter(user__isnull=True).count()
        
        # Calculate 7-day visits
        seven_day_visits = Visit.objects.filter(timestamp__gte=last_7_days)
        data['last_7_days']['visits'] = seven_day_visits.count()
        data['last_7_days']['unique'] = UniqueVisitor.objects.filter(last_visit__gte=last_7_days).count()
        
        # Calculate 30-day visits
        thirty_day_visits = Visit.objects.filter(timestamp__gte=last_30_days)
        data['last_30_days']['visits'] = thirty_day_visits.count()
        data['last_30_days']['unique'] = UniqueVisitor.objects.filter(last_visit__gte=last_30_days).count()
        
        # 4. Top 10 Pages by Visit Count
        top_pages = Visit.objects.values('path') \
            .annotate(page_count=Count('path')) \
            .order_by('-page_count')[:10]
            
        # 5. Top 10 most active authenticated users
        top_users = Visit.objects.filter(user__isnull=False).values('user__username') \
            .annotate(visit_count=Count('user__username')) \
            .order_by('-visit_count')[:10]

        context = self.each_context(request)
        context.update({
            'title': 'Traffic Statistics Overview',
            'data': data,
            'total_visits': total_visits,
            'total_unique_visitors': total_unique_visitors,
            'top_pages': top_pages,
            'top_users': top_users,
            'has_permission': True,
        })
        
        # Render a custom template (which we will define next)
        return render(request, 'admin/visits/traffic_stats.html', context)

# Initialize the custom admin site (optional, for advanced dashboard view)
# analytics_admin_site = AnalyticsAdmin(name='analytics_admin')

# If you use the custom admin site, remember to register models to it
# analytics_admin_site.register(Visit, VisitAdmin)
# analytics_admin_site.register(UniqueVisitor, UniqueVisitorAdmin)

# To use the custom view within the standard admin, we can modify the default admin index
# NOTE: For simplicity, let's stick to using the default admin site and displaying the raw data tables. 
# Creating a custom AdminSite requires changes in project urls.py, which is outside the app's scope.
# The user can already see the visit counts via the registered models (VisitAdmin, UniqueVisitorAdmin).
