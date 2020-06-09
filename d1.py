from flask import Flask
app=Flask(__name__)

@app.route("/")
def plots2p():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64

    from resonator_tools import circuit
    port1 = circuit.notch_port()
    port1.add_froms2p('c:/Users/3333.s2p',3,4,'realimag',fdata_unit=1e9,delimiter=None)
    port1.autofit()
    print("Fit results:", port1.fitresults)
    port1.plotall()
    print("single photon limit:", port1.get_single_photon_limit(diacorr=True), "dBm")
    print("photons in reso for input -140dBm:", port1.get_photons_in_resonator(-140,unit='dBm',diacorr=True), "photons")
    print("done")

    sio = BytesIO()
    plt.savefig(sio, format='png')
    data = base64.encodebytes(sio.getvalue()).decode()

    html = '''
       <html>
           <body>
               <img src="data:image/png;base64,{}" />
           </body>
        <html>
    '''

    plt.close()
    return html.format(data)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8000)
