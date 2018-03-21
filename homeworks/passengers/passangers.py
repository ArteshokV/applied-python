# -*- encoding: utf-8 -*-
def findPassanger(data, passangerName): # returns [number of train, number of car, number of man] or 0
    i = 0
    j=0
    k=0
    for train in data:
        for car in train['cars']:
            for man in car['people']:
                if (man == passangerName):
                    return [i, j, k]
                k=k+1
            j=j+1
            k=0
        i=i+1
        j=0
    return -1

def findTrain(data, trainName):
    i=0
    for train in data:
        if (train['name'] == trainName):
            return i
        i = i + 1
    return -1

def process(data, events, car):
    #print(data, '\n')
    #print(events, '\n')
    #print(car, '\n')

    for event in events:
        if (event['type'] == 'walk'):
            passangerLocation = findPassanger(data,event['passenger'])

            # Checkeing if passanger can walk and event is right
            if(passangerLocation == -1):
                return -1

            endCarLocation = passangerLocation[1] + event['distance']

            if (endCarLocation < 0) or (endCarLocation > len(data[passangerLocation[0]]['cars'])):
                return -1
            #Changing passanger place in train
            train = data[passangerLocation[0]]
            carsArray = train['cars']
            currentCar = carsArray[passangerLocation[1]]
            currentCarPassangersArray = currentCar['people']

            del currentCarPassangersArray[passangerLocation[2]] #removing passanger from current car

            futureCar = carsArray[endCarLocation]
            futureCarPassangersArray = futureCar['people']
            futureCarPassangersArray.append(event['passenger']) #adding passanger to a new car
            #print('New data: ', data)
        elif (event['type'] == 'switch'):
            #Checking if trains data are correct and fromTrain.cars >= 2
            fromTrainNumber = findTrain(data, event['train_from'])
            destinationTrainNumber = findTrain(data, event['train_to'])
            if (fromTrainNumber == -1) or (destinationTrainNumber == -1):
                return -1
            if (len(data[fromTrainNumber]['cars']) < event['cars']):
                return -1
            #Changing cars in trains
            fromTrainCarsArray = data[fromTrainNumber]['cars']
            fromTrainLength = len(fromTrainCarsArray)
            destinationTrainCarsArray = data[destinationTrainNumber]['cars']

            destinationTrainCarsArray.extend(fromTrainCarsArray[fromTrainLength-event['cars']:fromTrainLength])
            del fromTrainCarsArray[fromTrainLength-event['cars']:fromTrainLength]
            #print('New data: ', data)
        else:
            return -1

    #print(data)
    for train in data:
        for carTr in train['cars']:
            if(carTr['name'] == car):
                return len(carTr['people'])








    '''
    for train in data:
        print(train['name'])
        for car in train['cars']:
            print('\t{}'.format(car['name']))
            for man in car['people']:
                if()
                print('\t\t{}'.format(man))
    '''
    return -1