#include <TProof.h>
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

void run_KaonYield(Int_t RunNumber = 0, Int_t MaxEvent = 0, TString spec = "", TString detec = "")
{
  // Get RunNumber, MaxEvent, and current threshold if not provided.
  if(RunNumber == 0) {
    cout << "Enter a Run Number (-1 to exit): ";
    cin >> RunNumber;
    if( RunNumber<=0 ) return;
  }
  if(MaxEvent == 0) {
    cout << "\nNumber of Events to analyze: ";
    cin >> MaxEvent;
    if(MaxEvent == 0) {
      cerr << "...Invalid entry\n";
      exit;
    }
  }
  if(spec == "") {
    cout << "Enter spec (hms or shms): ";
    cin >> spec;
  }
  if(detec == "") {
    cout << "Enter detector: ";
    cin >> detec;
  }

  ofstream myfile1;
  myfile1.open ("kaonyieldVar", fstream::app);
  myfile1 << left << RunNumber << "   " << pscal << "   ";
  myfile1.close();

  TChain ch("T");
  ch.Add(Form("/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/ROOTfiles/%s_%s_PID_%i_%i.root",spec,detec,RunNumber,MaxEvent));
  TString option = Form("%i",RunNumber);

  TProof *proof = TProof::Open("workers=4");
  //proof->SetProgressDialog(0);  
  ch.SetProof();
  ch.Process(Form("%s_%s_efficiency.C+",spec,detec),option);
  proof->Close();
  
  TChain sc("TSH");
  ch.Add(Form("/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/ROOTfiles/%s_%s_PID_%i_%i.root",spec,detec,RunNumber,MaxEvent));
  sc.Process("HMS_Scalers.C+",option);
}
