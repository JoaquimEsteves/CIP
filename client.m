clc
clear all
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% The things that each group needs to change are identified by (*)%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% ESTABLISHING CONNECTION
fprintf('\n Receiver started! \n'); 
connection = tcpip('DESKTOP-49DVFN0',8881,'NetworkRole','Client'); %(*) Here you're going to put the server's IP and the port given by the manager

set(connection,'OutputBufferSize',500); 

set(connection,'InputBufferSize',500); 

set(connection,'Timeout',300);

fprintf('\n Waiting for connection.\n'); 

% VERIFY THE SUCCESS OF THE CONNECTION
try 

    fopen(connection);
    fprintf('\n Connection OK!\n'); 
    
catch

    disp('\n Connection failed!\n');

end
              
while true
    
    while connection.BytesAvailable == 0 
        
        pause(0.1)
        
    end
    
    DataReceived = fread(connection, connection.BytesAvailable,'char');
    fprintf('\n%s \n',DataReceived)
    
    DataReceived = strsplit(char(DataReceived'),'\n');
    
    for i = 1:length(DataReceived)
        
        DataRec = char(DataReceived(i));
        
        % HERE ADRESS THE MESSAGES FROM SUPERVISION
        % You have to change the if conditions to the possible orders you may
        % receive from the server. If necessary, add more elseif conditions.
        
        if strcmp(DataRec, 'WhoAreYou') % Welcome message
            
            message = uint8('Belt\n');  % (*)Insert here the name of your station as below.
                                        % StorageAndAssembly\n
                                        % Scorbot\n
                                        % AGV\n
                                        % Belt\n
                                        % RFID\n
                                        % QC\n
            
            fwrite(connection, message, 'uint8');
            fprintf('\n Supervision already knows who you are!\n')
            clear DataRec
            
        elseif strcmp(DataRec ,'[SUP]GOTO STORAGE') % (*) Change to one of the possible orders you can receive from the server.
            
            %(*) Run your function related to the order received.
            
            message = uint8('OK\n');
            fwrite(connection, message , 'uint8');
            clear DataRec
            
        elseif strcmp(DataRec, 'blablabla') % (*) Change to other possible order you can receive from the server.
            
            %(*) Run your function related to the order received.
            
            message = uint8('OK\n');
            fwrite(connection, message , 'uint8');
            clear DataRec
            
        elseif startsWith(DataRec, 'Welcome to the fam, fam!'); 
            
            fprintf('\n Here it comes!\n')
            clear DataRec
            
        else % Unpredicted message received
            
            fprintf('\n Something went wrong!\n')
            clear DataRec
            
        end
    end
    
    clear DataReceived

end

% CLOSE CONNECTION
fclose(connection)