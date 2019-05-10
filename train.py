import torch
import torch.nn as nn
import torch.utils.data as utils
import sys,os,json

n_in, n_h, n_out = 304, 500, 2

alldata = torch.load('traintest.pt')
x,y = torch.split(alldata, [304,1], dim=1)
y = y.long().view(-1)
#x = x.t()
#y = y.t()

print x.size(),y.size()

model = nn.Sequential(nn.Linear(n_in, n_h),
                     nn.Sigmoid(),
                     nn.Linear(n_h, n_out),
                     #nn.Sigmoid(),
                     #nn.Linear(n_h,n_out),
                     nn.Softmax())

criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

epoch = 1
while True:
    # Forward Propagation
    y_pred = model(x)
    # Compute and print loss
    loss = criterion(y_pred, y)
    print('epoch: ', epoch,' loss: ', loss.item())
    # Zero the gradients
    optimizer.zero_grad()
    
    # perform a backward pass (backpropagation)
    loss.backward()
    
    # Update the parameters
    optimizer.step()
    epoch += 1
    if epoch%100 == 0:
        torch.save(model.state_dict(), 'er.model')
