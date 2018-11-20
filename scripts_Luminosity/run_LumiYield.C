#include <TProof.h>
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

//void run_LumiYield(Int_t RunNumber = 0, Int_t MaxEvent = 0, Double_t threshold_cut = 2.5, Int_t pscal = 1)
void run_LumiYield(Int_t RunNumber = 0, Int_t MaxEvent = 0)
{

  if(RunNumber == 0) {
    cout << "Enter a run number (-1 to exit): ";
    cin >> RunNumber;
    if( RunNumber<=0 ) return;
  }

  if(MaxEvent == 0) {
    cout << "Enter number of events (-1 for all events): ";
    cin >> MaxEvent;
    if( RunNumber<=0 ) 
      MaxEvent = -1;
  }

  TChain ch("T");
  TChain sc("TSH");
  TString option;
  fstream REPORT_file;
  Int_t l_num = 0;
  string l;
  TString line_PS1, line_PS3;
  Int_t PS1, PS3;
  ofstream myfile1;


  REPORT_file.open (Form("/home/trottar/ResearchNP/ROOTAnalysis/REPORT_OUTPUT/COIN/PRODUCTION/KaonLT_replay_luminosity_coin_production_%i_%i.report",RunNumber,MaxEvent));

  if (REPORT_file.is_open()) {
    while (getline(REPORT_file,l)) {
      l_num++;
      if (l_num == 24) {
	line_PS1 = l;
      }
      if (l_num == 26) {
	line_PS3 = l;
      }
    }
  }
  
  REPORT_file.close();
  line_PS1 = line_PS1(13,line_PS1.Length());
  line_PS3 = line_PS3(13,line_PS3.Length());

  PS1 = line_PS1.Atoi();
  PS3 = line_PS3.Atoi();

  cout << "PS1 " << PS1 << " added\n";
  cout << "PS3 " << PS3 << " added\n";

  cout << Form("Using prescale factors: PS1 %i, PS3 %i\n",PS1,PS3);

  myfile1.open ("Yield_Data.dat", fstream::app);
  myfile1 << Form("%d ", RunNumber);
  myfile1.close();

  //Begin Counting Good Kaon Events

  ch.Add(Form("/lustre/expphy/volatile/hallc/spring17/trottar/ROOTfiles/KaonLT_Luminosity_coin_replay_production_%i_%i.root",RunNumber,MaxEvent));
 option = Form("%i.%i",PS1,PS3);
  

  sc.Add(Form("/lustre/expphy/volatile/hallc/spring17/trottar/ROOTfiles/KaonLT_Luminosity_coin_replay_production_%i_%i.root",RunNumber,MaxEvent));

 TProof *proof = TProof::Open("workers=4");
  //proof->SetProgressDialog(0);  
  ch.SetProof();
  ch.Process("LumiYield.C+",option);
  proof->Close();
  sc.Process("Scalers.C+",option);
}
