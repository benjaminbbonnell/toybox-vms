from django.db import models

# backend data: tax_codes, 
# foundational data: sites, org_units, charge codes
# user data: users, roles, permissions, 
#client config data: client profile, feature flags,
# client config settings: settings, approval workflows, timecard rules, overtime profiles, pay rules, invoice rules, fee profiles, custom fields, job templates
# transactional data: jobs, candidates, workers, work orders, timecards, invoices, payments, audit trails

# foundational data:

class Site(models.Model):
    site_code = models.CharField(max_length=10, unique=True)
    site_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    subdivision = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=200, blank=True, null=True)
    address_line2 = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.site_name

class OrgUnit(models.Model):
    org_unit_code = models.CharField(max_length=10, unique=True)
    org_unit_name = models.CharField(max_length=100)
    org_unit_parent_code = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    org_unit_owner_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.org_unit_name

class ChargeCode(models.Model):
    charge_code = models.CharField(max_length=10, unique=True)
    charge_code_name = models.CharField(max_length=200)
    charge_code_type = models.CharField(max_length=50)

    def __str__(self):
        return self.charge_code


#user data, ignore for now. Likely using Django Guardian for user management, but we can extend the user model to include additional fields as needed.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    preferred_first_name = models.CharField(max_length=30, blank=True, null=True)
    preferred_last_name = models.CharField(max_length=30, blank=True, null=True)
    supervisor_username = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='subordinates')
    home_org_unit_code = models.ForeignKey(OrgUnit, on_delete=models.SET_NULL, blank=True, null=True)
    all_org_unit_access = models.BooleanField(default=False)
    home_site_code = models.ForeignKey(Site, on_delete=models.SET_NULL, blank=True, null=True)
    all_site_access = models.BooleanField(default=False)
    home_charge_code = models.ForeignKey(ChargeCode, on_delete=models.SET_NULL, blank=True, null=True)
    all_charge_code_access = models.BooleanField(default=False)
    security_role = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.username

#client config data
class ClientProfile(models.Model):
    client_name = models.CharField(max_length=100)
    client_code = models.CharField(max_length=10, unique=True)
    client_logo_url = models.URLField(blank=True, null=True)
    client_contact_email = models.EmailField(blank=True, null=True)
    client_contact_phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.client_name

class FeatureFlag(models.Model):
    feature_name = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.feature_name

#client config settings
class Setting(models.Model):
    setting_name = models.CharField(max_length=100, unique=True)
    setting_value = models.TextField()

    def __str__(self):
        return self.setting_name

class ApprovalWorkflow(models.Model):
    workflow_name = models.CharField(max_length=100, unique=True)
    workflow_steps = models.JSONField()  # Store the steps as a JSON array

    def __str__(self):
        return self.workflow_name

class TimecardRule(models.Model):
    rule_name = models.CharField(max_length=100, unique=True)
    rule_definition = models.JSONField()  # Store the rule definition as a JSON object

    def __str__(self):
        return self.rule_name

class OvertimeProfile(models.Model):
    profile_name = models.CharField(max_length=100, unique=True)
    overtime_rules = models.JSONField()  # Store the overtime rules as a JSON object

    def __str__(self):
        return self.profile_name

class PayRule(models.Model):
    rule_name = models.CharField(max_length=100, unique=True)
    rule_definition = models.JSONField()  # Store the rule definition as a JSON object

    def __str__(self):
        return self.rule_name

class InvoiceRule(models.Model):
    rule_name = models.CharField(max_length=100, unique=True)
    rule_definition = models.JSONField()  # Store the rule definition as a JSON object

    def __str__(self):
        return self.rule_name

class FeeProfile(models.Model):
    profile_name = models.CharField(max_length=100, unique=True)
    fee_rules = models.JSONField()  # Store the fee rules as a JSON object

    def __str__(self):
        return self.profile_name

class CustomField(models.Model):
    field_name = models.CharField(max_length=100, unique=True)
    field_type = models.CharField(max_length=50)  # e.g., text, number, date, etc.
    field_definition = models.JSONField()  # Store additional field properties as a JSON object

    def __str__(self):
        return self.field_name

class JobTemplates(models.Model):
    template_name = models.CharField(max_length=100, unique=True)
    template_definition = models.JSONField()  # Store the template definition as a JSON object

    def __str__(self):
        return self.template_name

#transactional data
class Job(models.Model):
    job_id = models.CharField(max_length=20, unique=True)
    job_title = models.CharField(max_length=200)
    job_description = models.TextField(blank=True, null=True)
    org_unit_code = models.ForeignKey(OrgUnit, on_delete=models.SET_NULL, blank=True, )
    site_codes = models.ManyToManyField(Site, blank=True)
    charge_codes = models.ManyToManyField(ChargeCode, blank=True)
    owner_username = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='owned_jobs')
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    bill_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=False)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    approval_workflow = models.ForeignKey(ApprovalWorkflow, on_delete=models.SET_NULL, blank=True, null=True)
    timecard_rule = models.ForeignKey(TimecardRule, on_delete=models.SET_NULL, blank=True, null=True)
    overtime_profile = models.ForeignKey(OvertimeProfile, on_delete=models.SET_NULL, blank=True, null=True)
    pay_rule = models.ForeignKey(PayRule, on_delete=models.SET_NULL, blank=True, null=True)
    invoice_rule = models.ForeignKey(InvoiceRule, on_delete=models.SET_NULL, blank=True, null=True)
    fee_profile = models.ForeignKey(FeeProfile, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.job_title