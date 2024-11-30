from django import forms

from denjyauto.repairs.models import Repair, SensitiveRepairInfo


class RepairForm(forms.ModelForm):
    class Meta:
        model = Repair
        exclude = ('car',)


class SensitiveRepairInfoForm(forms.ModelForm):
    class Meta:
        model = SensitiveRepairInfo
        exclude = ('repair', )









