from ROOT import TFile, TH1F, TMath
import math

def process_pdf_uncertainties(root_file_path, histogram_name):
    file = TFile(root_file_path, "READ")
    
    h_nominal = file.Get(histogram_name)
    
    h_sys_uncertainty = h_nominal.Clone("h_sys_uncertainty")
    h_sys_uncertainty.Reset()
    
    for bin in range(1, h_nominal.GetNbinsX() + 1):
        pdf_variations = []
        for i in range(1, 101): 
            h_pdf_variation = file.Get("{}_pdf{}".format(histogram_name, i))
            if h_pdf_variation:
                pdf_variations.append(h_pdf_variation.GetBinContent(bin))
        
        # Calculate the RMS of the PDF variations for this bin
        if pdf_variations:
            mean = sum(pdf_variations) / len(pdf_variations)
            rms = math.sqrt(sum((xi - mean) ** 2 for xi in pdf_variations) / len(pdf_variations))
            h_sys_uncertainty.SetBinContent(bin, h_nominal.GetBinContent(bin))  # Set central value
            h_sys_uncertainty.SetBinError(bin, rms)  # Set the PDF uncertainty as the error
    
    # Do similar processes for other systematic uncertainties like JER/JEC, scale variations, etc., and sum them in quadrature
    
    file.Close()
    return h_sys_uncertainty

# Adapt this function for other systematics and aggregate them in quadrature
# Remember to replace 'root_file_path' and 'histogram_name' with your actual file path and histogram names

# Example usage
root_file_path = "path/to/your/root_file.root"
histogram_name = "your_histogram_name_here"
h_sys_uncertainty_pdf = process_pdf_uncertainties(root_file_path, histogram_name)

# To visualize or further process `h_sys_uncertainty_pdf`, use it in your plotting scripts.
