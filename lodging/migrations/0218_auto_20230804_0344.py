from django.db import migrations, models

def create_agent_access_instances(apps, schema_editor):
    Agents = apps.get_model('lodging', 'Agents')
    Stays = apps.get_model('lodging', 'Stays')
    
    for obj in Stays.objects.all():
        for agent in obj.agents.all():
            agent_access = Agents.objects.create(user=agent, stay=obj, approved=True)
            obj.agents.remove(agent)
        

class Migration(migrations.Migration):

    dependencies = [
        ('lodging', '0217_agents'),
    ]

    operations = [
        migrations.RunPython(create_agent_access_instances),
    ]
