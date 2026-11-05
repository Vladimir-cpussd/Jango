from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from .models import Course, Module, Subject, Content, Text, File, Image, Video


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

    def has_module_permission(self, request):
        return request.user.is_superuser


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


# --- ФОРМА С ЗАГРУЗКОЙ ---
class ContentAdminForm(forms.ModelForm):
    upload_file = forms.FileField(required=False, label='Загрузить файл (PDF, Word и т.д.)')

    class Meta:
        model = Content
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded_file = self.cleaned_data.get('upload_file')
        
        if uploaded_file:
            new_file = File.objects.create(
                title=uploaded_file.name, 
                file=uploaded_file,
                owner=self.current_user
            )
            instance.object_id = new_file.id
            instance.content_type = ContentType.objects.get_for_model(File)
        
        if commit:
            instance.save()
        return instance

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    form = ContentAdminForm
    list_display = ['item', 'module', 'content_type']
    list_filter = ['content_type']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user  
        return form

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(module__course__owner=request.user)

    def has_module_permission(self, request):
        return request.user.is_superuser


class ContentInline(admin.StackedInline):
    model = Content
    form = ContentAdminForm
    extra = 1

    # Передаем request.user в форму для каждого инлайна
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        class CustomFormSet(formset):
            def _construct_form(inner_self, i, **kwargs):
                kwargs['current_user'] = request.user
                return super()._construct_form(i, **kwargs)
        return CustomFormSet


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    inlines = [ContentInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__owner=request.user)


# --- СКРЫВАЕМ РАЗДЕЛЫ ДЛЯ ПРЕПОДОВ ---
@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return request.user.is_superuser