#include <TProof.h>
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

void plot_LumiYield(Int_t numRuns = 0){
  
  if(numRuns==0){
    cout << "\nPlease enter number of runs... ";
    cin >> numRuns;
    
    if(numRuns==0){
      cerr << "Invalid entry\n";
      //exit;
      
    }
  }

  TString outputpdf;
  fstream inputFile;
  Int_t line_num = 0;
  string line;
  TString line_rn[numRuns];
  Int_t runNum[numRuns];
  
  inputFile.open ("/home/trottar/ResearchNP/ROOTAnalysis/kaonlt_analysis/lumiscan/inputRuns");
  
  if (inputFile.is_open()) {
    while (getline(inputFile,line)) {
      line_rn[line_num] = line;
      line_num++;
    }
  }
  
  inputFile.close();
  // line_PS1 = line_PS1(13,line_PS1.Length());
  cout << "Plotting run numbers..\n";

  for(Int_t i=0;i<numRuns;i++){
   runNum[i] = line_rn[i].Atoi();
   cout << runNum[i] << " ";
  }

  TString foutname = Form("/home/trottar/Analysis/hallc_replay/UTIL_KAONLT/scripts_Luminosity/OUTPUT/Luminosity_PID_all_%i-%i",runNum[0],runNum[numRuns-1]);
  //TString foutname = Form("/home/trottar/Analysis/hallc_replay/UTIL_KAONLT/scripts_Luminosity/OUTPUT/Luminosity_PID_Carbon_%i-%i",runNum[0],runNum[numRuns-1]);
  //TString foutname = Form("/home/trottar/Analysis/hallc_replay/UTIL_KAONLT/scripts_Luminosity/OUTPUT/Luminosity_PID_LH2_%i-%i",runNum[0],runNum[numRuns-1]);

  cout << "\n";

  TH1F *h_ecut_before[numRuns]; 
  TH1F *h_ecut_after[numRuns];
  TH1F *h_ecut_eff[numRuns];
  TH1F *p_ecut_before[numRuns];
  TH1F *p_ecut_after[numRuns];
  TH1F *p_ecut_eff[numRuns];

  TH1F *p_dp_before[numRuns];
  TH1F *p_dp_after[numRuns];
  TH1F *h_dp_before[numRuns];
  TH1F *h_dp_after[numRuns];

  TH1F *p_th_before[numRuns];
  TH1F *p_th_after[numRuns];
  TH1F *h_th_before[numRuns];
  TH1F *h_th_after[numRuns];

  TH1F *p_ph_before[numRuns];
  TH1F *p_ph_after[numRuns];
  TH1F *h_ph_before[numRuns];
  TH1F *h_ph_after[numRuns];

  TH1F *p_show_before[numRuns];
  TH1F *p_show_after[numRuns];
  TH1F *h_show_before[numRuns];
  TH1F *h_show_after[numRuns];

  TH2F *h_cer_cal_before[numRuns];
  TH2F *h_cer_cal_after[numRuns];
  TH2F *p_hg_cal_before[numRuns]; 
  TH2F *p_hg_cal_after[numRuns];
  
  TH1F *h_track_before[numRuns];
  TH1F *h_track_after[numRuns];
  TH1F *h_etrack_before[numRuns];
  TH1F *h_etrack_after[numRuns]; 
  TH1F *p_track_before[numRuns]; 
  TH1F *p_track_after[numRuns];   
  TH1F *p_hadtrack_before[numRuns];
  TH1F *p_hadtrack_after[numRuns];
  TH1F *p_pitrack_before[numRuns];
  TH1F *p_pitrack_after[numRuns]; 
  TH1F *p_Ktrack_before[numRuns]; 
  TH1F *p_Ktrack_after[numRuns];  
  TH1F *p_ptrack_before[numRuns]; 
  TH1F *p_ptrack_after[numRuns];  

  TH1F *EventType[numRuns];  
  TH1F *bcm_before[numRuns]; 
  TH1F *bcm_after[numRuns];  

  TH1F *EDTM[numRuns];     
  TH1F *HMS_EDTM[numRuns]; 
  TH1F *SHMS_EDTM[numRuns];
  TH1F *TRIG1[numRuns];    
  TH1F *TRIG3[numRuns];    
  TH1F *TRIG5[numRuns];    
  TH1F *TRIG1_cut[numRuns];
  TH1F *TRIG3_cut[numRuns];
  TH1F *TRIG5_cut[numRuns];


  for(Int_t i=0;i<numRuns;i++){
  TFile *rootFile = new TFile(Form("OUTPUT/Luminosity_PID_%i.root",runNum[i]));

  h_ecut_before[i] = (TH1F*)rootFile->Get("h_ecut_before");
  h_ecut_after[i]  = (TH1F*)rootFile->Get("h_ecut_after");
  h_ecut_eff[i]    = (TH1F*)rootFile->Get("h_ecut_eff");
  p_ecut_before[i] = (TH1F*)rootFile->Get("p_ecut_before");
  p_ecut_after[i]  = (TH1F*)rootFile->Get("p_ecut_after");
  p_ecut_eff[i]    = (TH1F*)rootFile->Get("p_ecut_eff");

  p_dp_before[i]   = (TH1F*)rootFile->Get("p_dp_before");
  p_dp_after[i]    = (TH1F*)rootFile->Get("p_dp_after");  
  h_dp_before[i]   = (TH1F*)rootFile->Get("h_dp_before");
  h_dp_after[i]    = (TH1F*)rootFile->Get("h_dp_after");

  p_th_before[i]   = (TH1F*)rootFile->Get("p_th_before");
  p_th_after[i]    = (TH1F*)rootFile->Get("p_th_after");
  h_th_before[i]   = (TH1F*)rootFile->Get("h_th_before");
  h_th_after[i]    = (TH1F*)rootFile->Get("h_th_after");

  p_ph_before[i]   = (TH1F*)rootFile->Get("p_ph_before");
  p_ph_after[i]    = (TH1F*)rootFile->Get("p_ph_after");
  h_ph_before[i]   = (TH1F*)rootFile->Get("h_ph_before");
  h_ph_after[i]    = (TH1F*)rootFile->Get("h_ph_after");

  p_show_before[i] = (TH1F*)rootFile->Get("p_show_before");
  p_show_after[i]  = (TH1F*)rootFile->Get("p_show_after");
  h_show_before[i] = (TH1F*)rootFile->Get("h_show_before");
  h_show_after[i]  = (TH1F*)rootFile->Get("h_show_after");

  h_cer_cal_before[i] = (TH2F*)rootFile->Get("h_cer_cal_before");  
  h_cer_cal_after[i]  = (TH2F*)rootFile->Get("h_cer_cal_after"); 
  p_hg_cal_before[i]  = (TH2F*)rootFile->Get("p_hg_cal_before");
  p_hg_cal_after[i]   = (TH2F*)rootFile->Get("p_hg_cal_after"); 
  
  h_track_before[i]   = (TH1F*)rootFile->Get("h_track_before");
  h_track_after[i]    = (TH1F*)rootFile->Get("h_track_after");
  h_etrack_before[i]  = (TH1F*)rootFile->Get("h_etrack_before");
  h_etrack_after[i]   = (TH1F*)rootFile->Get("h_etrack_after");
  p_track_before[i]   = (TH1F*)rootFile->Get("p_track_before");
  p_track_after[i]    = (TH1F*)rootFile->Get("p_track_after");
  p_hadtrack_before[i]= (TH1F*)rootFile->Get("p_hadtrack_before");
  p_hadtrack_after[i] = (TH1F*)rootFile->Get("p_hadtrack_after");
  p_pitrack_before[i] = (TH1F*)rootFile->Get("p_pitrack_before");
  p_pitrack_after[i]  = (TH1F*)rootFile->Get("p_pitrack_after");
  p_Ktrack_before[i]  = (TH1F*)rootFile->Get("p_Ktrack_before");
  p_Ktrack_after[i]   = (TH1F*)rootFile->Get("p_Ktrack_after");
  p_ptrack_before[i]  = (TH1F*)rootFile->Get("p_ptrack_before");
  p_ptrack_after[i]   = (TH1F*)rootFile->Get("p_ptrack_after");

  EventType[i]   = (TH1F*)rootFile->Get("Event_Type");
  bcm_before[i]  = (TH1F*)rootFile->Get("bcm_before");
  bcm_after[i]   = (TH1F*)rootFile->Get("bcm_after");

  EDTM[i]      = (TH1F*)rootFile->Get("EDTM");
  HMS_EDTM[i]  = (TH1F*)rootFile->Get("HMS_EDTM");
  SHMS_EDTM[i] = (TH1F*)rootFile->Get("SHMS_EDTM");
  TRIG1[i]     = (TH1F*)rootFile->Get("TRIG1");
  TRIG3[i]     = (TH1F*)rootFile->Get("TRIG3");
  TRIG5[i]     = (TH1F*)rootFile->Get("TRIG5");
  TRIG1_cut[i] = (TH1F*)rootFile->Get("TRIG1_cut");
  TRIG3_cut[i] = (TH1F*)rootFile->Get("TRIG3_cut");
  TRIG5_cut[i] = (TH1F*)rootFile->Get("TRIG5_cut");

  }
 
  outputpdf = foutname + ".pdf";

  TCanvas *c_plot;
  TLegend *leg;
  leg = new TLegend(.74,.73,.96,.94, "Run Numbers");
  //leg = new TLegend(.74,.63,.96,.94, "Run Numbers");
  c_plot = new TCanvas("c_plot","PID");
  for(Int_t i=0;i<numRuns;i++){
    leg->AddEntry(h_cer_cal_before[i],Form("%i",runNum[i]), "l");
    leg->SetTextSize(0.033);
    if(i==0){
      c_plot->Divide(2,2);
      c_plot->cd(1);
      h_cer_cal_before[i]->GetXaxis()->SetTitle("H_cal_etotnorm");
      h_cer_cal_before[i]->GetYaxis()->SetTitle("H_cer_npeSum");
      h_cer_cal_before[i]->SetMarkerColor(48-i*2);
      h_cer_cal_before[i]->Draw();
      //h_cer_cal_before[i]->SetStats(kFALSE);
      //leg->Draw();
      c_plot->cd(2);
      h_cer_cal_after[i]->GetXaxis()->SetTitle("H_cal_etotnorm");
      h_cer_cal_after[i]->GetYaxis()->SetTitle("H_cer_npeSum");
      h_cer_cal_after[i]->SetMarkerColor(48-i*2);
      h_cer_cal_after[i]->Draw();
      //h_cer_cal_after[i]->SetStats(kFALSE);
      //leg->Draw();
      c_plot->cd(3);
      p_hg_cal_before[i]->GetXaxis()->SetTitle("P_cal_etotnorm");
      p_hg_cal_before[i]->GetYaxis()->SetTitle("P_hgcer_npeSum");
      p_hg_cal_before[i]->SetMarkerColor(48-i*2);
      p_hg_cal_before[i]->Draw();
      //p_hg_cal_before[i]->SetStats(kFALSE);
      //leg->Draw();
      c_plot->cd(4);
      p_hg_cal_after[i]->GetXaxis()->SetTitle("P_cal_etotnorm");
      p_hg_cal_after[i]->GetYaxis()->SetTitle("P_hgcer_npeSum");
      p_hg_cal_after[i]->SetMarkerColor(48-i*2);
      p_hg_cal_after[i]->Draw();
      //p_hg_cal_after[i]->SetStats(kFALSE);
      //leg->Draw(); 
    }else{
      c_plot->cd(1);
      h_cer_cal_before[i]->GetXaxis()->SetTitle("H_cal_etotnorm");
      h_cer_cal_before[i]->GetYaxis()->SetTitle("H_cer_npeSum");
      h_cer_cal_before[i]->SetMarkerColor(48-i*2);
      h_cer_cal_before[i]->Draw("SAME");
      //h_cer_cal_before[i]->SetStats(kFALSE);
      //leg->Draw("SAME");
      c_plot->cd(2);
      h_cer_cal_after[i]->GetXaxis()->SetTitle("H_cal_etotnorm");
      h_cer_cal_after[i]->GetYaxis()->SetTitle("H_cer_npeSum");
      h_cer_cal_after[i]->SetMarkerColor(48-i*2);
      h_cer_cal_after[i]->Draw("SAME");
      //h_cer_cal_after[i]->SetStats(kFALSE);
      //leg->Draw("SAME");
      c_plot->cd(3);
      p_hg_cal_before[i]->GetXaxis()->SetTitle("P_cal_etotnorm");
      p_hg_cal_before[i]->GetYaxis()->SetTitle("P_hgcer_npeSum");
      p_hg_cal_before[i]->SetMarkerColor(48-i*2);
      p_hg_cal_before[i]->Draw("SAME");
      //p_hg_cal_before[i]->SetStats(kFALSE);
      //leg->Draw("SAME");
      c_plot->cd(4);
      p_hg_cal_after[i]->GetXaxis()->SetTitle("P_cal_etotnorm");
      p_hg_cal_after[i]->GetYaxis()->SetTitle("P_hgcer_npeSum");
      p_hg_cal_after[i]->SetMarkerColor(48-i*2);
      p_hg_cal_after[i]->Draw("SAME");
      //p_hg_cal_after[i]->SetStats(kFALSE);
      //leg->Draw("SAME")
    }
  }
  c_plot->Print(outputpdf +"(");

  TCanvas *c_ID_cut;
  TLegend *leg2;
  leg2 = new TLegend(.74,.73,.96,.94, "Run Numbers");
  //leg2 = new TLegend(.74,.63,.96,.94, "Run Numbers");
  c_ID_cut = new TCanvas("c_ID_cut","Particle ID Information");
  for(Int_t i=0;i<numRuns;i++){
    leg2->AddEntry(h_ecut_before[i],Form("%i",runNum[i]), "l");
    leg2->SetTextSize(0.033);
    if(i==0){
      c_ID_cut->Divide(3,2);
      c_ID_cut->cd(1);
      h_ecut_before[i]->SetLineColor(48-i*2);
      h_ecut_before[i]->Draw();
      h_ecut_before[i]->SetStats(kFALSE);
      leg2->Draw();
      c_ID_cut->cd(2);
      h_ecut_after[i]->SetLineColor(48-i*2);
      h_ecut_after[i]->Draw();
      h_ecut_after[i]->SetStats(kFALSE);
      leg2->Draw();
      c_ID_cut->cd(3);
      h_ecut_eff[i]->SetLineColor(48-i*2);
      h_ecut_eff[i]->Draw();
      h_ecut_eff[i]->SetStats(kFALSE);
      leg2->Draw();
      c_ID_cut->cd(4);
      gPad->SetLogy();
      p_ecut_before[i]->SetLineColor(48-i*2);
      p_ecut_before[i]->Draw();
      p_ecut_before[i]->SetStats(kFALSE);
      leg2->Draw();
      c_ID_cut->cd(5);
      gPad->SetLogy();
      p_ecut_after[i]->SetLineColor(48-i*2);
      p_ecut_after[i]->Draw();
      p_ecut_after[i]->SetStats(kFALSE);
      leg2->Draw();
      c_ID_cut->cd(6);
      gPad->SetLogy();
      p_ecut_eff[i]->SetLineColor(48-i*2);
      p_ecut_eff[i]->Draw();
      p_ecut_eff[i]->SetStats(kFALSE);
      leg2->Draw();
    }else{
      c_ID_cut->cd(1);
      h_ecut_before[i]->SetLineColor(48-i*2);
      h_ecut_before[i]->Draw("SAME");
      h_ecut_before[i]->SetStats(kFALSE);
      leg2->Draw("SAME");
      c_ID_cut->cd(2);
      h_ecut_after[i]->SetLineColor(48-i*2);
      h_ecut_after[i]->Draw("SAME");
      h_ecut_after[i]->SetStats(kFALSE);
      leg2->Draw("SAME");
      c_ID_cut->cd(3);
      h_ecut_eff[i]->SetLineColor(48-i*2);
      h_ecut_eff[i]->Draw("SAME");
      h_ecut_eff[i]->SetStats(kFALSE);
      leg2->Draw("SAME");
      c_ID_cut->cd(4);
      gPad->SetLogy();
      p_ecut_before[i]->SetLineColor(48-i*2);
      p_ecut_before[i]->Draw("SAME");
      p_ecut_before[i]->SetStats(kFALSE);
      leg2->Draw("SAME");
      c_ID_cut->cd(5);
      gPad->SetLogy();
      p_ecut_after[i]->SetLineColor(48-i*2);
      p_ecut_after[i]->Draw("SAME");
      p_ecut_after[i]->SetStats(kFALSE);
      leg2->Draw("SAME");
      c_ID_cut->cd(6);
      gPad->SetLogy();
      p_ecut_eff[i]->SetLineColor(48-i*2);
      p_ecut_eff[i]->Draw("SAME"); 
      p_ecut_eff[i]->SetStats(kFALSE); 
      leg2->Draw("SAME");
    }
  }
  c_ID_cut->Print(outputpdf);
 
  TCanvas *c_etot_cut;
  TLegend *leg3;
  leg3 = new TLegend(.74,.73,.96,.94, "Run Numbers");
  //leg3 = new TLegend(.74,.63,.96,.94, "Run Numbers");
  c_etot_cut = new TCanvas("c_etot_cut","Calorimeter Energy Information");
  for(Int_t i=0;i<numRuns;i++){
    leg3->AddEntry(h_show_before[i],Form("%i",runNum[i]), "l");
    leg3->SetTextSize(0.033);
    if(i==0){
      c_etot_cut->Divide(2,2);
      c_etot_cut->cd(1);
      h_show_before[i]->SetLineColor(48-i*2);
      h_show_before[i]->Draw();
      h_show_before[i]->SetStats(kFALSE);
      leg3->Draw();
      c_etot_cut->cd(2);
      h_show_after[i]->SetLineColor(48-i*2);
      h_show_after[i]->Draw();
      h_show_after[i]->SetStats(kFALSE);
      leg3->Draw();
      c_etot_cut->cd(3);
      p_show_before[i]->SetLineColor(48-i*2);
      p_show_before[i]->Draw();
      p_show_before[i]->SetStats(kFALSE);
      leg3->Draw();
      c_etot_cut->cd(4);
      p_show_after[i]->SetLineColor(48-i*2);
      p_show_after[i]->Draw();
      p_show_after[i]->SetStats(kFALSE);
      leg3->Draw();
    }else{
      c_etot_cut->cd(1);
      h_show_before[i]->SetLineColor(48-i*2);
      h_show_before[i]->Draw("SAME");
      h_show_before[i]->SetStats(kFALSE);
      leg3->Draw("SAME");
      c_etot_cut->cd(2);
      h_show_after[i]->SetLineColor(48-i*2);
      h_show_after[i]->Draw("SAME");
      h_show_after[i]->SetStats(kFALSE);
      leg3->Draw("SAME");
      c_etot_cut->cd(3);
      p_show_before[i]->SetLineColor(48-i*2);
      p_show_before[i]->Draw("SAME");
      p_show_before[i]->SetStats(kFALSE);
      leg3->Draw("SAME");
      c_etot_cut->cd(4);
      p_show_after[i]->SetLineColor(48-i*2);
      p_show_after[i]->Draw("SAME");
      p_show_after[i]->SetStats(kFALSE);
      leg3->Draw("SAME");
    }
  }
  c_etot_cut->Print(outputpdf);
  
  TCanvas *c_track_cut;
  TLegend *leg4;
  leg4 = new TLegend(.74,.73,.96,.94, "Run Numbers");
  //leg4 = new TLegend(.74,.63,.96,.94, "Run Numbers");
  c_track_cut = new TCanvas("c_track_cut","Good Track Information");
  for(Int_t i=0;i<numRuns;i++){
    leg4->AddEntry(h_track_before[i],Form("%i",runNum[i]), "l");
    leg4->SetTextSize(0.033);
    if(i==0){
      c_track_cut->Divide(2,2);
      c_track_cut->cd(1);
      gPad->SetLogy();
      h_track_before[i]->SetLineColor(48-i*2);
      h_track_before[i]->Draw();
      h_track_before[i]->SetStats(kFALSE);
      leg4->Draw();
      c_track_cut->cd(2);
      gPad->SetLogy();
      h_track_after[i]->SetLineColor(48-i*2);
      h_track_after[i]->Draw();
      h_track_after[i]->SetStats(kFALSE);
      leg4->Draw();
      c_track_cut->cd(3);
      gPad->SetLogy();
      p_hadtrack_before[i]->SetLineColor(48-i*2);
      p_hadtrack_before[i]->Draw();
      p_hadtrack_before[i]->SetStats(kFALSE);
      leg4->Draw();
      c_track_cut->cd(4);
      gPad->SetLogy();
      p_hadtrack_after[i]->SetLineColor(48-i*2);
      p_hadtrack_after[i]->Draw();
      p_hadtrack_after[i]->SetStats(kFALSE);
      leg4->Draw();
    }else{
      c_track_cut->cd(1);
      gPad->SetLogy();
      h_track_before[i]->SetLineColor(48-i*2);
      h_track_before[i]->Draw("SAME");
      h_track_before[i]->SetStats(kFALSE);
      leg4->Draw("SAME");
      c_track_cut->cd(2);
      gPad->SetLogy();
      h_track_after[i]->SetLineColor(48-i*2);
      h_track_after[i]->Draw("SAME");
      h_track_after[i]->SetStats(kFALSE);
      leg4->Draw("SAME");
      c_track_cut->cd(3);
      gPad->SetLogy();
      p_hadtrack_before[i]->SetLineColor(48-i*2);
      p_hadtrack_before[i]->Draw("SAME");
      p_hadtrack_before[i]->SetStats(kFALSE);
      leg4->Draw("SAME");
      c_track_cut->cd(4);
      gPad->SetLogy();
      p_hadtrack_after[i]->SetLineColor(48-i*2);
      p_hadtrack_after[i]->Draw("SAME");
      p_hadtrack_after[i]->SetStats(kFALSE);
      leg4->Draw("SAME");
    }
  }
  c_track_cut->Print(outputpdf);

  TCanvas *c_bcm_cut;
  TLegend *leg5;
  leg5 = new TLegend(.74,.73,.96,.94, "Run Numbers");
  //leg5 = new TLegend(.74,.63,.96,.94, "Run Numbers");
  c_bcm_cut = new TCanvas("c_bcm_cut","Beam Current Monitor Information");
  for(Int_t i=0;i<numRuns;i++){
    leg5->AddEntry(bcm_before[i],Form("%i",runNum[i]), "l");
    leg5->SetTextSize(0.033);
    if(i==0){
      c_bcm_cut->Divide(2,1);
      c_bcm_cut->cd(1);  
      bcm_before[i]->SetLineColor(48-i*2);
      bcm_before[i]->Draw();
      bcm_before[i]->SetStats(kFALSE);
      leg5->Draw();
      c_bcm_cut->cd(2);
      bcm_after[i]->SetLineColor(48-i*2);
      bcm_after[i]->Draw();
      bcm_after[i]->SetStats(kFALSE);
      leg5->Draw();
    }else{
      c_bcm_cut->cd(1);  
      bcm_before[i]->SetLineColor(48-i*2);
      bcm_before[i]->Draw("SAME");
      bcm_before[i]->SetStats(kFALSE);
      leg5->Draw("SAME");
      c_bcm_cut->cd(2);
      bcm_after[i]->SetLineColor(48-i*2);
      bcm_after[i]->Draw("SAME");
      bcm_after[i]->SetStats(kFALSE);
      leg5->Draw("SAME");
    }
  }
  c_bcm_cut->Print(outputpdf);

  TCanvas *c_EventType; 
  TLegend *leg6;
  leg6 = new TLegend(.74,.73,.96,.94, "Run Numbers");
  //leg6 = new TLegend(.74,.63,.96,.94, "Run Numbers");
  c_EventType = new TCanvas("Event Type","Event Type Information");
  for(Int_t i=0;i<numRuns;i++){
    leg6->AddEntry(EventType[i],Form("%i",runNum[i]), "l");
    leg6->SetTextSize(0.033);
    if(i==0){
      c_EventType->Divide(2,2);
      c_EventType->cd(1);
      EventType[i]->SetLineColor(48-i*2);
      EventType[i]->Draw();
      EventType[i]->SetStats(kFALSE);
      leg6->Draw();
      c_EventType->cd(2);
      EDTM[i]->SetLineColor(48-i*2);
      EDTM[i]->Draw();
      EDTM[i]->SetStats(kFALSE);
      leg6->Draw();
      c_EventType->cd(3);
      TRIG1[i]->SetLineColor(48-i*2);
      TRIG1[i]->Draw();
      TRIG1[i]->SetStats(kFALSE);
      leg6->Draw();
      c_EventType->cd(4);
      TRIG3[i]->SetLineColor(48-i*2);
      TRIG3[i]->Draw();
      TRIG3[i]->SetStats(kFALSE);
      leg6->Draw();
    }else{
      c_EventType->cd(1);
      EventType[i]->SetLineColor(48-i*2);
      EventType[i]->Draw("SAME");
      EventType[i]->SetStats(kFALSE);
      leg6->Draw("SAME");
      c_EventType->cd(2);
      EDTM[i]->SetLineColor(48-i*2);
      EDTM[i]->Draw("SAME");
      EDTM[i]->SetStats(kFALSE);
      leg6->Draw("SAME");
      c_EventType->cd(3);
      TRIG1[i]->SetLineColor(48-i*2);
      TRIG1[i]->Draw("SAME");
      TRIG1[i]->SetStats(kFALSE);
      leg6->Draw("SAME");
      c_EventType->cd(4);
      TRIG3[i]->SetLineColor(48-i*2);
      TRIG3[i]->Draw("SAME");
      TRIG3[i]->SetStats(kFALSE);
      leg6->Draw("SAME");
    }
  }
  c_EventType->Print(outputpdf +")");

}
