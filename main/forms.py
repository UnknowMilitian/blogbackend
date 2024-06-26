# forms.py
from django import forms
from .models import Blog, BlogCategory


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "category", "text", "image"]

    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update(
            {
                "class": "p-[1rem] bg-slate-800 rounded-md text-white border-2 border-transparent focus:border-green-300 outline-none box-border w-full",
                "placeholder": "Title",
            }
        )
        self.fields["category"].widget.attrs.update(
            {
                "class": "p-[0.9rem] bg-slate-800 rounded-md text-gray-400 border-2 border-transparent focus:border-green-300 outline-none box-border w-full"
            }
        )
        self.fields["text"].widget.attrs.update(
            {
                "class": "block p-[1rem] bg-slate-800 rounded-md text-white border-2 border-transparent focus:border-green-300 outline-none box-border w-full",
                "placeholder": "Write your thoughts here...",
            }
        )
        self.fields["image"].widget.attrs.update(
            {"class": "hidden", "id": "dropzone-file"}
        )
        self.fields["category"].empty_label = "Category"
        self.fields["category"].choices = [("", "Category")] + list(
            self.fields["category"].choices
        )[1:]
