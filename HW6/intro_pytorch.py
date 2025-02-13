import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

def main():
    train_loader = get_data_loader()
    test_loader = get_data_loader(training=False)
    print(type(train_loader))
    print(train_loader.dataset)
    model = build_model()
    print(model)
    train_model(model, train_loader, nn.CrossEntropyLoss, 0)
    evaluate_model(model, test_loader, nn.CrossEntropyLoss, show_loss = True)
    test_images = next(iter(test_loader))[0]
    predict_label(model, test_images, 1)

def get_data_loader(training = True):
    """
    TODO: implement this function.

    INPUT: 
        An optional boolean argument (default value is True for training dataset)

    RETURNS:
        Dataloader for the training set (if training = True) or the test set (if training = False)
    """
    #loader
    custom_transform=transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
        ])
    train_set = datasets.FashionMNIST('./data',train=True, download=True, 
                                      transform=custom_transform)
    test_set=datasets.FashionMNIST('./data', train=False,
                                    transform=custom_transform)
    if training is True:
        loader = torch.utils.data.DataLoader(train_set, batch_size = 64)
    else:
        loader = torch.utils.data.DataLoader(test_set, batch_size = 64)
    return loader



def build_model():
    """
    TODO: implement this function.

    INPUT: 
        None

    RETURNS:
        An untrained neural network model
    """
    model = nn.Sequential(
        nn.Flatten(),
        nn.Linear(in_features=28*28, out_features=128),
        nn.ReLU(),
        nn.Linear(in_features=128, out_features=64),
        nn.ReLU(),
        nn.Linear(in_features=64, out_features=10)
    )
    return model
    




def train_model(model, train_loader, criterion, T):
    """
    TODO: implement this function.

    INPUT: 
        model - the model produced by the previous function
        train_loader  - the train DataLoader produced by the first function
        criterion   - cross-entropy 
        T - number of epochs for training

    RETURNS:
        None
    """
    criterion = nn.CrossEntropyLoss()
    opt = optim.SGD(model.parameters(), lr=0.001, momentum=0.9) 
    epoch_counter = 0
    for epoch in range(5):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            opt.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            opt.step()
            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_accuracy = 100 * correct/total
        print(f"Train Epoch: {epoch}    Accuracy: {correct}/{total}({epoch_accuracy:.2f}%) Loss: {epoch_loss:.3f}")
        epoch_counter +=1 

            
            
            
    


def evaluate_model(model, test_loader, criterion, show_loss = True):
    """
    TODO: implement this function.

    INPUT: 
        model - the the trained model produced by the previous function
        test_loader    - the test DataLoader
        criterion   - cropy-entropy 

    RETURNS:
        None
    """
    model.eval()
    criterion = nn.CrossEntropyLoss()
    correct = 0
    total = 0
    running_loss = 0.0
    accuracy = 0.0
    with torch.no_grad():
        for data, labels in test_loader:
            outputs = model(data)
            loss = criterion(outputs, labels)
            running_loss += loss.item() * data.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    running_loss /= len(test_loader.dataset)
    accuracy = 100 * (correct/total)
    if show_loss:
        print(f"Average loss: {running_loss:.4f}")
    print(f"Accuracy: {accuracy:.2f}%")
    


def predict_label(model, test_images, index):
    """
    TODO: implement this function.

    INPUT: 
        model - the trained model
        test_images   -  a tensor. test image set of shape Nx1x28x28
        index   -  specific index  i of the image to be tested: 0 <= i <= N - 1


    RETURNS:
        None
    """
    model.eval()
    
    with torch.no_grad():
        outputs = model(test_images[index].unsqueeze(0))
        probs = F.softmax(outputs, dim=1)
        
        top_prob, top_indices = torch.topk(probs, 3)
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle Boot']

        for i in range(3):
            class_index = top_indices[0][i].item()
            prob = top_prob[0][i].item() * 100
            class_name = class_names[class_index]
            print(f"{class_name}: {prob:.2f}%")


if __name__ == '__main__':
    '''
    Feel free to write your own test code here to exaime the correctness of your functions. 
    Note that this part will not be graded.
    '''
    main()
    criterion = nn.CrossEntropyLoss()
