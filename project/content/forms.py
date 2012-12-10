from django import forms
from tinymce import widgets as tinymce_widgets
import models

TINYMCE_OPTIONS = {  
  'theme':'advanced',
  'theme_advanced_toolbar_location' : "top",
  'theme_advanced_toolbar_align' : "left",
  'theme_advanced_buttons1' : "fullscreen,save,separator,bold,italic,underline"
            +",separator,justifyleft,justifycenter,justifyright"
            +",separator,bullist,numlist,outdent,indent"
            +",separator,undo,redo,separator,link,unlink,media"
            +",separator,cleanup,removeformat,code",#,help,anchor",
  'theme_advanced_buttons2' : "tablecontrols",
  'theme_advanced_buttons3_add' : "pastetext,pasteword,selectall",
  'theme_advanced_buttons3' : "",
  'auto_cleanup_word' : 1,
  'removeformat_select' : '[border|class|style|height|width]',
  'plugins' : "table,save,advhr,iespell,insertdatetime,contextmenu,"
              +"fullscreen,media,paste",
  'file_browser_callback': 'CustomFileBrowser',
 
}



class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = models.Article
        widgets = {
          #'body':tinymce_widgets.TinyMCE(attrs={'cols': 80, 'rows': 20}, mce_attrs=TINYMCE_OPTIONS),
          'title': forms.TextInput(attrs={'size':'80'}),
        }

class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = models.News
        widgets = {
            'body':tinymce_widgets.TinyMCE(attrs={'cols': 80, 'rows': 20}, mce_attrs=TINYMCE_OPTIONS),
            'headline': forms.TextInput(attrs={'size':'80'}),
        }    
