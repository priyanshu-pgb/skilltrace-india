from core.management.commands.seed_demo_data import Command as SeedDemoDataCommand

class Command(SeedDemoDataCommand):
    help = 'Alias for seed_demo_data to ensure compatibility with Render deployment commands'
