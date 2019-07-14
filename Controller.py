import asyncio
import queue
import json
# import RPi.GPIO as GPIO


class drink_controller():

    def __init__(self):
        self.drinkQueue = queue.Queue()
        self.is_busy = False
        with open('./static/config.json') as f:
            config = json.load(f)

        self.secPerOunce = config['secPerOunce']
        self.drinks = {}
        for item in config['drinks']:
            self.drinks[item['id']] = {
                'displayName': item['displayName'],
                'recipe': item['recipe']
            }
        self.ingredients = {}
        all_pins = []
        for item in config['ingredients']:
            self.ingredients[item['id']] = item['pin']
            all_pins.append(item['pin'])

        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(all_pins, GPIO.OUT)

    async def asyncPin(self, pin, delay):
        """
        open the pin, then use non-blocking sleep to wait for specified time
        then deactivate pin

        delay -- the time to leave the pin open in seconds
        """
        print('activating pin {}'.format(pin))
        # GPIO.output(pin, GPIO.HIGH)
        await asyncio.sleep(delay)
        print('deactivating pin {}'.format(pin))
        # GPIO.output(pin, GPIO.LOW)

        return

    async def make(self, drinkPins):
        # creates tasks for each of the pins in the recipe, then executes the loop
        pins = drinkPins
        tasks = []
        for pin in pins:
            task = asyncio.ensure_future(self.asyncPin(*pin))
            tasks.append(task)
        await asyncio.gather(*tasks)
        print('Drink Done!')
        return

    def makeNext(self, loop):
        # pulls next drink in queue and calls make()
        asyncio.set_event_loop(loop)
        if not self.drinkQueue.empty():
            self.is_busy = True
            drink = self.drinkQueue.get()
            print('Now making "{}"...'.format(drink['displayName']))
            drinkPins = []

            # translate ingredients to (pin, time) tuples
            for ingredient, amount in drink['recipe'].items():
                drinkPins.append((self.ingredients[ingredient], amount * self.secPerOunce))
            loop.run_until_complete(self.make(drinkPins))
            self.is_busy = False
        else:
            print('Oops! There aren\'t any drinks in the queue!')

    def add_drink(self, drinkId):
        drink = self.drinks[drinkId]
        missing = []
        for ingredient in drink['recipe']:
            if ingredient not in self.ingredients:
                missing.append(ingredient)

        if missing:
            return 'I\'m missing the following ingredients: {}'.format((', ').join(missing))
        else:
            self.drinkQueue.put(drink)
            return drink['displayName'] + ' added to queue.'


if __name__ == '__main__':

    drink = {
        "displayName": "Vodka Tonic",
        "recipe": {
            "vodka": 1,
            "tonic": 5
        }
    }

    controller = drink_controller()
    controller.drinkQueue.put(drink)
    controller.makeNext()

    # GPIO.cleanup()
