# serializers.py
from rest_framework import serializers
from .models import Product, Component, Process, Machine

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['id', 'name', 'machine_type', 'state']  # Añadido id

class ProcessSerializer(serializers.ModelSerializer):
    machines_info = MachineSerializer(many=True, read_only=True, source="machines")  # Cambiado a plural
    machines = serializers.PrimaryKeyRelatedField(
        queryset=Machine.objects.all(),
        many=True,  # Añadido many=True para ManyToMany
        write_only=True
    )
    
    class Meta:
        model = Process
        fields = ['id', 'name', 'process_type', 'process_source', 'assigned_to', 'machines_info', 'machines']  # Añadido id y name, y la coma faltante

    def create(self, validated_data):
        machines_data = validated_data.pop('machines')
        process = Process.objects.create(**validated_data)
        process.machines.set(machines_data)
        return process

    def update(self, instance, validated_data):
        machines_data = validated_data.pop('machines', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if machines_data is not None:
            instance.machines.set(machines_data)
        
        return instance

class ComponentSerializer(serializers.ModelSerializer):
    manufacturing_process = serializers.PrimaryKeyRelatedField(
        queryset=Process.objects.all(),
        many=True,  # Añadido many=True para ManyToMany
        write_only=True
    )
    manufacturing_process_info = ProcessSerializer(many=True, read_only=True, source="manufacturing_process")  # Cambiado a many=True
    
    class Meta:
        model = Component
        fields = ['id', 'name', 'comp_id', 'description', 'component_type', 'manufacturing_process_info', 'manufacturing_process']  # Añadido id

    def create(self, validated_data):
        processes_data = validated_data.pop('manufacturing_process')
        component = Component.objects.create(**validated_data)
        component.manufacturing_process.set(processes_data)
        return component

    def update(self, instance, validated_data):
        processes_data = validated_data.pop('manufacturing_process', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if processes_data is not None:
            instance.manufacturing_process.set(processes_data)
        
        return instance

class ProductSerializer(serializers.ModelSerializer):
    components_info = ComponentSerializer(many=True, read_only=True, source='components')
    components = serializers.PrimaryKeyRelatedField(
        queryset=Component.objects.all(),
        many=True,
        write_only=True
    )
    
    class Meta:
        model = Product
        fields = ['id', 'op_value', 'name', 'description', 'priority', 
                 'status', 'components', 'components_info', 'quantity',
                 'start_date', 'end_date', 'updated_at', 'notes', 'progress']  # Añadido progress

    def create(self, validated_data):
        components_data = validated_data.pop('components')
        product = Product.objects.create(**validated_data)
        product.components.set(components_data)
        return product

    def update(self, instance, validated_data):
        components_data = validated_data.pop('components', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if components_data is not None:
            instance.components.set(components_data)
        
        return instance