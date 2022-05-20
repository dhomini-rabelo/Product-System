from django.core.management import BaseCommand



    


class BasicCommand(BaseCommand):
    
    def show_actions(self, actions: list[str]):
        bar = str('-' * 100)

        print(bar, '\n')

        print('Actions')
        for action in actions:
            print(f' ->  {action}')

        print('\n', bar)
