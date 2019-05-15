#include <TProof.h>
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

void Q3W2Right()
{
  TChain ch("T");
  ch.Add("~/Analysis/hallc_replay_kaonlt/ROOTfiles/KaonLT_coin_replay_production_4865_-1.root");
  ch.Add("~/Analysis/hallc_replay_kaonlt/ROOTfiles/KaonLT_coin_replay_production_4866_-1.root");
  ch.Add("~/Analysis/hallc_replay_kaonlt/ROOTfiles/KaonLT_coin_replay_production_4867_-1.root");
  ch.Add("~/Analysis/hallc_replay_kaonlt/ROOTfiles/KaonLT_coin_replay_production_4868_-1.root");

  TProof *proof = TProof::Open("workers=4");
  //proof->SetProgressDialog(0);  
  ch.SetProof();
  ch.Process("~/Analysis/hallc_replay_kaonlt/scripts_KaonYield/KaonYield_Q3W2.C+","1");
  proof->Close();
  
}
