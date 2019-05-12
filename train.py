import torch
import torch.nn as nn
import torch.utils.data as utils
import sys,os,json

n_in, n_h, n_out = 304, 200, 2

alldata = torch.load('traintest_normalised.pt')
x,y = torch.split(alldata, [304,1], dim=1)
x = x.cuda()
y = y.long().view(-1)
#x = x.t()
#y = y.t()

print x.size(),y.size()

train_split_size = int(0.8 * x.size()[0])
test_split_size = x.size()[0] - train_split_size

x_train,x_test = torch.split(x, [train_split_size, test_split_size], dim=0)
y_train,y_test = torch.split(y, [train_split_size, test_split_size], dim=0)

x_train = x_train.cuda()
x_test = x_test.cuda()
y_train = y_train.cuda()
y_test = y_test.cuda()


model = nn.Sequential(nn.Linear(n_in, n_h),
                     nn.ReLU(),
                     nn.Linear(n_h, n_h),
                     nn.ReLU(),
                     nn.Linear(n_h,n_out),
                     nn.Softmax()).cuda()

criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

epoch = 1
while True:
    # Forward Propagation
    y_pred = model(x_train)
    # Compute and print loss
    loss = criterion(y_pred, y_train)
    # Zero the gradients
    optimizer.zero_grad()
    # perform a backward pass (backpropagation)
    loss.backward()
    # Update the parameters
    optimizer.step()
    #validate

    epoch += 1
    if epoch%1000 == 0:
        print('epoch: ', epoch,' loss: ', loss.item())
        model.eval()
        y_test_pred = model(x_test)
        correct = 0
        for i in range(test_split_size):
            predres = 1.0 - (y_test_pred[i][0]>0.5)
            if torch.eq(predres.long(),y_test[i]):
                correct += 1

        print("Acc = %f"%(correct/float(test_split_size)))
        model.train()
        torch.save(model.state_dict(), 'er.model')
