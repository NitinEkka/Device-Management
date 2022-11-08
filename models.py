from django.db import models
from farms.models import * 
from pdc.models import DomeParameters
from django.db.models.signals import pre_save, post_save
from users.models import User
from django.dispatch import receiver
from config.models import Config
# Create your models here.

# list_values = list(Config.objects.filter(key='starter type'))
# list_value1 = list(Config.objects.filter(key='starter type'))
# tup_starter_choice = tuple(
#     zip(
#         list_values, list_value1
#     )
# )
# print(list_values)


# field_name = 'value'
# obj = Config.objects.last()
# field_value = getattr(obj, field_name)
# list1 = field_value["motortype"]
# list2 = field_value["motortype"]

# tup_starter_choice = tuple(
#     zip(
#         list1, list2
#     )
# )

# print(tup_starter_choice)

STATUS_CHOICES = (
    ("pcb_ready","pcb_ready"),
    ("pcb_basic_testing","pcb_basic_testing"),
    ("pcb_function_testing","pcb_function_testing"),
    ("pcb_assembly_testing","pcb_assembly_testing"),
    ("final_testing","final_testing"),
    ("ready_for_shipping","ready_for_shipping"),
    ("in_transit","in_transit"),
    ("in_stock","in_stock"),
    ("deployed","deployed"),
    ("paired","paired"),
)

DEVICE_TYPE = (
    ("1PH","1PH"),
    ("3PH","3PH"),   
)

PRODUCT_TYPE = (
    ("1","1"),
    ("2","2"),   
)

LED_TYPE = (
    ("rgb","rgb"),
    ("single","single"),   
)

SSR_TRIGGER = (
    ("5A","5A"),
    ("40A","40A"),   
)

STARTER_TYPE = (
    ("ssr","ssr"),
    ("dol","dol"),   
)

APPLICATION = (
    ("irrigation","irrigation"),
    ("exhaust","exhaust"),
    ("fogger","fogger"),   
)

HPRANGE = (
    ("2hp","2hp"),
    ("3hp","3hp"),
    ("5hp","5hp"),   
)

LEDCHECK = (
    ("glowing","glowing"),
    ("off","off"),
    ("blinking","blinking"),
)


class DeviceManagement(models.Model):
    """
    Model to Store Device details
    """
    

    atmega_pcb_version = models.CharField(max_length=35)
    stack_pcb_version = models.CharField(max_length=35)
    pcb_id = models.CharField(max_length=10 , primary_key=True)
    esp_chip_id = models.CharField(max_length=35)
    assembly_version = models.CharField(max_length=35)
    atmega_program_version = models.CharField(max_length=35)
    esp_program_version = models.CharField(max_length=35)
    starter_type = models.CharField(max_length=35)
    meta_data = models.JSONField
    current_status = models.CharField(
        max_length=20,
        choices = STATUS_CHOICES,
        default = 'pcb_ready',
        )
        
    debug = models.BooleanField(default=False)
    testing_officer = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    device_type = models.CharField(
        max_length=4,
        choices = DEVICE_TYPE,
    )
    product_type = models.CharField(
        max_length=5,
        choices = PRODUCT_TYPE,
    )

    def __str__(self):
        return self.pcb_id


class BasicTesting(models.Model):
    pcb_id = models.ForeignKey(DeviceManagement, on_delete=models.PROTECT)
    pcb_board_version = models.CharField(max_length=20)
    visual_check = models.BooleanField(default=False)
    continuity = models.BooleanField(default=False)
    power_supply_test = models.BooleanField(default=False)
    atmega_program = models.CharField(max_length=30)
    esp32_program = models.CharField(max_length=30)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.pcb_id

class FunctionalTesting(models.Model):
    pcb_id = models.ForeignKey(DeviceManagement, on_delete=models.PROTECT)
    esp_chip_id = models.CharField(max_length=30)
    atmega_chip_id = models.CharField(max_length=30)
    led = models.CharField(
        max_length=10,
        choices = LED_TYPE,
    )
    ssr_trigger_test = models.CharField(
        max_length=10,
        choices = SSR_TRIGGER,
    )
    water_level_test = models.BooleanField(default=False)
    temperature_test = models.BooleanField(default=False)
    rtc_check = models.CharField(max_length=10)
    rtc_after_reset = models.CharField(max_length=10)
    vr_voltage = models.IntegerField
    vy_voltage = models.IntegerField
    vb_voltage = models.IntegerField
    solenoid_feedback = models.CharField(max_length=20)
    trigger_button = models.BooleanField(default=False)
    starting_current = models.CharField(max_length=30)
    load_on_current = models.CharField(max_length=30)
    load_off_current = models.CharField(max_length=30)
    current_test = models.BooleanField(default=False)
    esp_atmega_comm = models.BooleanField(default=False)
    esp_led = models.BooleanField(default=False)
    esp_reset = models.BooleanField(default=False)
    atmega_reset = models.BooleanField(default=False)
    atmega_reset_button = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.pcb_id


class BoxAssembly(models.Model):

    pcb_id = models.ForeignKey(DeviceManagement, on_delete=models.PROTECT)
    wiring = models.BooleanField(default=False)
    continuity = models.BooleanField(default=False)
    esp_programming = models.CharField(max_length=30)
    esp_ver = models.CharField(max_length=30)
    atmega_programming = models.CharField(max_length=30)
    starter_type = models.CharField(
        max_length=5,
        choices = STARTER_TYPE,
    )
    set_configuration = models.CharField(max_length=50)
    solenoid_test = models.BooleanField(default=False)
    lead_test_manual = models.CharField(max_length=80)
    ryb_current_value = models.IntegerField
    button = models.BooleanField(default=False)
    rtc = models.CharField(max_length=20)
    load_test_timer_using_minutes = models.CharField(max_length=10)
    load_test_on_off = models.BooleanField(default=False)
    status_parameters = models.CharField(max_length=20)
    error_code_test = models.BooleanField(default=False)
    device_id = models.CharField(max_length=10)
    remarks = models.CharField(max_length=50)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.pcb_id


class Shipping(models.Model):
    box_id = models.ForeignKey(DeviceManagement, on_delete=models.PROTECT)
    place = models.CharField(max_length=10)
    mode_of_transport = models.CharField(max_length=15)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.box_id

class Deployment(models.Model):
    box_id = models.ForeignKey(DeviceManagement, on_delete=models.PROTECT)
    farm_id = models.ForeignKey(Farm, on_delete=models.PROTECT)
    application = models.CharField(
        max_length=10,
        choices = APPLICATION,
    )
    hp_range = models.CharField(
        max_length=4,
        choices= HPRANGE,
    )
    dome = models.ForeignKey(DomeParameters, on_delete=models.PROTECT)
    input_voltage_op_testing = models.CharField(max_length=10)
    board_led_check = models.CharField(
        max_length=15,
        choices=LEDCHECK
    )
    manual_on_off = models.BooleanField(default=False)
    current_value_multimeter = models.IntegerField
    current_value_mqtt = models.IntegerField
    remote_on_off = models.BooleanField(default=False)
    set_configuration = models.CharField(max_length=20)
    timer_on_off = models.BooleanField(default=False)
    remarks = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.box_id


class StatusChange(models.Model):
    device_id = models.TextField()
    old_status = models.TextField()
    new_status = models.TextField()
    created_by = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    
    def device_id_post_save(sender, instance, **kwargs):
        StatusChange.objects.create(device_id=instance.pcb_id)
    post_save.connect(device_id_post_save, sender=DeviceManagement)  

    def new_status_record(sender, instance, **kwargs):
        StatusChange.objects.update(new_status=instance.current_status)
    post_save.connect(new_status_record, sender=DeviceManagement)      

    def created_by_record(sender, instance, **kwargs):
        StatusChange.objects.update(created_by=instance.testing_officer)
    post_save.connect(created_by_record, sender=DeviceManagement)     
    
    
    # def new_status_record(sender, instance, created, **kwargs):
    #     if created:
    #         field_name = 'current_status'
    #         obj = DeviceManagement.objects.last()
    #         field_value = getattr(obj, field_name)
    #         StatusChange.filter(pk=instance.pk).update(new_status=field_value)
    # post_save.connect(new_status_record, sender=DeviceManagement)

    
    # def device_id_post_save(sender, instance, created,**kwargs):
    #     if created:
    #         field_name = 'pcb_id'
    #         obj = DeviceManagement.objects.last()
    #         field_value = getattr(obj, field_name)
    #         StatusChange.objects.create(device_id=field_value)
    # post_save.connect(device_id_post_save, sender=DeviceManagement)


    # def created_by_records(sender, instance, created, **kwargs):
    #     if created:
    #         field_name = 'testing_officer'
    #         obj = DeviceManagement.objects.last()
    #         field_value = getattr(obj, field_name)
    #         StatusChange.filter(pk=instance.pk).update(created_by=field_value)
    # post_save.connect(created_by_records, sender=DeviceManagement)


    # if StatusChange.new_status == 'pcb_ready':
    #     StatusChange.old_status = 'In Production'
    # if StatusChange.new_status == 'pcb_basic_testing':
    #     StatusChange.old_status = 'pcb_ready'   
    # if StatusChange.new_status == 'pcb_function_testing':
    #     StatusChange.old_status = 'pcb_basic_testing'    
    # if StatusChange.new_status == 'pcb_assembly_testing':
    #     StatusChange.old_status = 'pcb_function_testing'
    # if StatusChange.new_status == 'final_testing':
    #     StatusChange.old_status = 'pcb_assembly_testing'   
    # if StatusChange.new_status == 'ready_for_shipping':
    #     StatusChange.old_status = 'final_testing'
    # if StatusChange.new_status == 'in_transit':
    #     StatusChange.old_status = 'ready_for_shipping'       
    # if StatusChange.new_status == 'in_stock':
    #     StatusChange.old_status = 'in_transit'    
    # if StatusChange.new_status == 'deployed':
    #     StatusChange.old_status = 'in_stock'  
    # if StatusChange.new_status == 'paired':
    #     StatusChange.old_status = 'deployed'      


    def __str__(self):
        return self.device_id               
        
    


