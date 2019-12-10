#include <TProof.h>
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

void run_KaonYield(Int_t RunNumber = 0, Int_t MaxEvent = 0, const char* spec = "", const char* detec = "", Double_t threshold_cut = 5, Int_t pscal = 1)
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
  // if(spec == "") {
  //   cout << "Enter spec (hms or shms): ";
  //   cin >> spec;
  // }
  // if(detec == "") {
  //   cout << "Enter detector: ";
  //   cin >> detec;
  // }
  
  TChain ch("T");
  ch.Add(Form("/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/ROOTfiles/PID_%i_%i.root",RunNumber,MaxEvent));
  TString option = Form("%i",RunNumber);
  
  TProof *proof = TProof::Open("workers=4");
  //proof->SetProgressDialog(0);  
  ch.SetProof();
  ch.Process(Form("%s_%s_efficiency.C+",spec,detec),option);
  proof->Close();
  
  TChain sc("TSH");
  ch.Add(Form("/u/group/c-kaonlt/USERS/trottar/hallc_replay_lt/UTIL_KAONLT/ROOTfiles/PID_%i_%i.root",RunNumber,MaxEvent));
  sc.Process("HMS_Scalers.C+",option);
}
