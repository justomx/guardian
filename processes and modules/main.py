import time
from mainruntime import ProcessRunner
from plconfig import FolderUpperCleaner  
from verifiers import inst_verify, send_message, process_registrant
import reports as rs
import schedule
import runpy

try:

    """
        Este módulo serve estritamente para fins de:
            - Gerenciar tarefas
    """

    class ReportGroup:

        def __init__(self):
            self.last_mile =[rs.MReport01,
                rs.MReport02,
                rs.MReport03,
                rs.MReport04,
                rs.MReport05,
                rs.MReport06,
                ]
            self.onmaps =[rs.MReport10,
                rs.MReport11,
                rs.GReport01
                ]
            self.growth_redundant =[#rs.MReport14,
                rs.MReport16,
                ]
            self.growth_performance =[#rs.AReport01,
                #rs.AReport02,
                rs.MReport38,
                rs.MReport39,
                rs.MReport40,
                rs.MReport41,
                rs.MReport42,
                ]
            self.growth_ecommerce =[rs.MReport12,
                #rs.MReport13,
                #rs.MReport14,
                rs.MReport15,
                ]
            self.funil =[#rs.MReport18,
              #  rs.MReport19,
                rs.MReport20,
                rs.MReport23,
                rs.MReport24,
              #  rs.MReport26, desligado
                ]
            self.bases_cx =[rs.GReport08,
                rs.PReport01,
                rs.MReport28,
                rs.ZReport05,
                rs.ZReport06,
                rs.ZReport07,
                rs.ZReport08,
                rs.ZReport09,
                rs.ZReport10,
                rs.ZReport11,
                rs.GReport15,
                rs.GReport16,
            ]
            self.experiencia_do_cliente=[rs.MReport29,
                rs.MReport30,
                rs.MReport37,
                rs.GReport02,
                rs.GReport03,
                rs.GReport10,
            ]
            self.motoristas =[#rs.MReport31,
               # rs.MReport32,
                rs.GReport04,
                rs.GReport05,
                rs.GReport06,
                rs.GReport07,
                rs.LReport01,
            ]
            self.funil_de_ops =[rs.ZReport01,
                rs.ZReport02,
                rs.ZReport03,
                rs.ZReport04,
            ]
            self.growth_real_time =[rs.MReport35,
             #Chrome   rs.MReport36,
            ]
            self.relatorio_merma =[rs.GReport11,
                rs.GReport12,
                rs.GReport13,
                rs.GReport14,
            ]
            self.mapa_abastecimento =[rs.MReport45,
                rs.MReport46,
                rs.MReport48,
                rs.MReport62
            ]

    class Manager:

        def __init__(self):
            self.current_list = []
            self.error_list = []

        def set_reports(self,metabase_list):
            self.current_list = metabase_list

        def errors_reset(self):
            self.error_list=[]

        def switch(self,report_set):
            self.set_reports(report_set)
            self.run_job()

            self.current_list = []

        def run_and_verify(self, report):
            cl = FolderUpperCleaner()
            cl.clean_downloads()
            self.process_runner=ProcessRunner(report)
            self.process_runner.process_sorting()
            if self.process_runner.error:
                self.error_handler(report,report.channel)
            else:
                pass
            return inst_verify(report.default_destination_path)

        def message_sender(self):
            self.message="Bom dia <!channel> tivemos falhas de extração pra esses reports"
            if self.error_list:
                all = "".join(self.error_list)
                send_message(self.message + all, 'bot_channel')

        def error_handler(self, report, channel):
            if report.instant_notification == True:
                send_message('Olá <!channel>, houve falha na extração do relatório '+report.name+' está sendo feita um nova rodagem do processo.',channel)
                if not self.run_and_verify(report):
                    send_message('Olá <!channel>, infelizmente a tentativa de extração não deu certo.',channel)
                else:
                    send_message('Olá <!channel>, a tentativa de extração deu certo.',channel)
                    return
            if report.instant_notification == False and report.forced_try == True:
                if not self.run_and_verify(report):
                    self.error_list.append('\n    - '+report.name)
                else:
                    return
            else:
                self.error_list.append('\n    - '+report.name)
                return

        def run_job(self):
            for c in self.current_list:
                report = c()
                channel=report.channel
                if self.run_and_verify(report):
                    continue
                else:
                    self.error_handler(report,channel)

    def etl_routines():
        e='etl_routines'
        runpy.run_path(path_name=e+'/etlroutine13.py') # appsflyer
        runpy.run_path(path_name=e+'/etlroutine01.py') # delivery - all bases
        runpy.run_path(path_name=e+'/etlroutine03.py') # all bases and other google sheets data load
        runpy.run_path(path_name=e+'/etlroutine04.py') # botmaker file
        runpy.run_path(path_name=e+'/etlroutine05.py') # unilever sales by sku file
        runpy.run_path(path_name=e+'/etlroutine06.py') # unilever sales file upload
        runpy.run_path(path_name=e+'/etlroutine07.py') # cupom data load to gsheets
        runpy.run_path(path_name=e+'/etlroutine08.py') # lg data load to gsheets
        runpy.run_path(path_name=e+'/etlroutine09.py') # unilever stock data generation and load
        runpy.run_path(path_name=e+'/etlroutine10.py') # ambev sales file upload
        runpy.run_path(path_name=e+'/etlroutine12.py') # placed orders upload to gsheets
        runpy.run_path(path_name=e+'/etlroutine15.py') # ifood products info

    managermb= Manager()
    switch = managermb.switch
    reportst = ReportGroup()    
    
    def workdays():
        e='etl_routines'
        v='validations'
        cl=FolderUpperCleaner()
        
        print('Workdays Mode')
        schedule.every().day.at("00:00").do(managermb.errors_reset)
        schedule.every().day.at("00:05").do(switch,reportst.funil_de_ops)
        schedule.every().day.at("00:30").do(switch,[rs.MReport43])  
        schedule.every().day.at("01:00").do(switch,reportst.onmaps)
        schedule.every().day.at("01:35").do(switch,reportst.funil)
        schedule.every().day.at("02:35").do(switch,reportst.growth_redundant)
        schedule.every().day.at("03:00").do(switch,reportst.growth_ecommerce)
        schedule.every().day.at("03:40").do(switch,reportst.bases_cx)  
        schedule.every().day.at("04:15").do(switch,reportst.motoristas)
        schedule.every().day.at("05:25").do(switch,reportst.experiencia_do_cliente) 
        schedule.every().day.at("06:00").do(switch,reportst.growth_performance)
        schedule.every().day.at("06:35").do(etl_routines)     
        schedule.every().day.at("06:45").do(switch,reportst.relatorio_merma)     
        schedule.every().day.at("05:55").do(cl.last_mile_set)
        schedule.every().day.at("06:20").do(managermb.message_sender)
        schedule.every().day.at("06:01").do(switch,reportst.last_mile)
        schedule.every().day.at("06:01").do(switch,reportst.mapa_abastecimento)
        schedule.every().day.at("07:00").do(switch,reportst.last_mile) 
        schedule.every().day.at("07:10").do(runpy.run_path,path_name=e+'/etlroutine08.py') #lg etl gsheets
        schedule.every().day.at("07:30").do(switch,[rs.GReport17]) #cupom verificação download
        schedule.every().day.at("07:38").do(runpy.run_path,path_name=v+'/validation01.py') #cupom category validation
        schedule.every().day.at("08:00").do(switch,reportst.last_mile)
        schedule.every().day.at("09:00").do(switch,reportst.last_mile)
        schedule.every().day.at("10:00").do(switch,reportst.last_mile)
        schedule.every().day.at("10:25").do(switch,[rs.MReport61]) #cupom 
        schedule.every().day.at("10:35").do(runpy.run_path,path_name=e+'/etlroutine14.py') #cupom etl mx
        schedule.every().day.at("10:37").do(switch,[rs.GReport24]) #cupom classfication pending mx
        schedule.every().day.at("10:39").do(runpy.run_path,path_name=v+'/validation02.py') #cupom category validation mx
        schedule.every().day.at("11:00").do(switch,reportst.last_mile)
        schedule.every().day.at("12:00").do(switch,reportst.last_mile)
        schedule.every().day.at("12:25").do(switch,[rs.MReport41]) #cupom
        schedule.every().day.at("13:00").do(switch,reportst.last_mile)
        schedule.every().day.at("13:30").do(switch,[rs.GReport17]) #cupom verificação download
        schedule.every().day.at("13:35").do(runpy.run_path,path_name=e+'/etlroutine07.py') #cupom etl
        schedule.every().day.at("13:38").do(runpy.run_path,path_name=v+'/validation01.py') #cupom category validation
        schedule.every().day.at("14:00").do(switch,reportst.last_mile)
        schedule.every().day.at("15:00").do(switch,reportst.last_mile) 
        schedule.every().day.at("15:25").do(switch,[rs.MReport61]) #cupom
        schedule.every().day.at("15:35").do(runpy.run_path,path_name=e+'/etlroutine14.py') #cupom etl mx
        schedule.every().day.at("15:37").do(switch,[rs.GReport24]) #cupom classfication pending mx
        schedule.every().day.at("15:39").do(runpy.run_path,path_name=v+'/validation02.py') #cupom category validation mx
        schedule.every().day.at("16:00").do(switch,reportst.last_mile)
        schedule.every().day.at("17:00").do(switch,reportst.last_mile)
        schedule.every().day.at("17:25").do(switch,[rs.MReport41]) #cupom
        schedule.every().day.at("17:30").do(switch,[rs.GReport17]) #cupom download
        schedule.every().day.at("17:35").do(runpy.run_path,path_name=e+'/etlroutine07.py') #cupom etl
        schedule.every().day.at("17:38").do(runpy.run_path,path_name=v+'/validation01.py') #cupom category validation
        schedule.every().day.at("18:00").do(switch,reportst.last_mile)
        schedule.every().day.at("19:00").do(switch,reportst.last_mile)
        schedule.every().day.at("20:00").do(switch,reportst.last_mile)
        schedule.every().day.at("20:25").do(switch,[rs.MReport61]) #cupom
        schedule.every().day.at("20:35").do(runpy.run_path,path_name=e+'/etlroutine14.py') #cupom etl mx
        schedule.every().day.at("20:37").do(switch,[rs.GReport24]) #cupom classfication pending mx
        schedule.every().day.at("20:39").do(runpy.run_path,path_name=v+'/validation02.py') #cupom category validation mx
        schedule.every().day.at("21:00").do(switch,reportst.last_mile)
        schedule.every().day.at("00:25").do(switch,[rs.GReport09]) #merma são domingos - entender o porque de termos essa automatização
        schedule.every().day.at("07:45").do(switch,[rs.MReport33]) #gestao à vista 
        schedule.every().day.at("08:45").do(switch,[rs.MReport33])
        schedule.every().day.at("09:45").do(switch,[rs.MReport33])
        schedule.every().day.at("11:45").do(switch,[rs.MReport33])
        schedule.every().day.at("13:45").do(switch,[rs.MReport33])
        schedule.every().day.at("15:45").do(switch,[rs.MReport33])
        schedule.every().day.at("17:45").do(switch,[rs.MReport33])
        schedule.every().day.at("19:45").do(switch,[rs.MReport33])
        schedule.every().day.at("21:45").do(switch,[rs.MReport33])
        schedule.every().day.at("22:45").do(switch,[rs.MReport33])
        schedule.every().day.at("23:45").do(switch,[rs.MReport33])
        schedule.every().day.at("10:45").do(switch,[rs.MReport47]) #gestao à vista MX
        schedule.every().day.at("12:45").do(switch,[rs.MReport47])
        schedule.every().day.at("14:45").do(switch,[rs.MReport47])
        schedule.every().day.at("16:45").do(switch,[rs.MReport47])
        schedule.every().day.at("18:45").do(switch,[rs.MReport47])
        schedule.every().day.at("20:45").do(switch,[rs.MReport47])
        schedule.every().day.at("22:45").do(switch,[rs.MReport47])
        schedule.every().day.at("00:40").do(switch,[rs.MReport47])
        schedule.every().day.at("10:47").do(runpy.run_path,path_name=e+'/etlroutine11.py') #gestao à vista MX to GSheets
        schedule.every().day.at("12:47").do(runpy.run_path,path_name=e+'/etlroutine11.py')
        schedule.every().day.at("14:47").do(runpy.run_path,path_name=e+'/etlroutine11.py')
        schedule.every().day.at("16:47").do(runpy.run_path,path_name=e+'/etlroutine11.py')
        schedule.every().day.at("18:47").do(runpy.run_path,path_name=e+'/etlroutine11.py')
        schedule.every().day.at("20:47").do(runpy.run_path,path_name=e+'/etlroutine11.py')
        schedule.every().day.at("22:47").do(runpy.run_path,path_name=e+'/etlroutine11.py')
        schedule.every().day.at("00:45").do(runpy.run_path,path_name=e+'/etlroutine11.py')
        schedule.every().day.at("23:45").do(switch,[rs.MReport34]) #base de vendas por sku status e periodo
        schedule.every().day.at("06:35").do(switch,[rs.MReport08]) #funil pedidos ops
        schedule.every().day.at("07:35").do(switch,[rs.MReport08])
        schedule.every().day.at("09:35").do(switch,[rs.MReport08])
        schedule.every().day.at("11:35").do(switch,[rs.MReport08])
        schedule.every().day.at("13:35").do(switch,[rs.MReport08])
        schedule.every().day.at("15:35").do(switch,[rs.MReport08])
        schedule.every().day.at("17:35").do(switch,[rs.MReport08])
        schedule.every().day.at("19:35").do(switch,[rs.MReport08])
        schedule.every().day.at("08:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("09:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("11:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("13:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("15:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("17:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("19:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("21:13").do(switch,reportst.growth_real_time)
        schedule.every().day.at("22:13").do(switch,reportst.growth_real_time)
                
        while True:
            schedule.run_pending()
            time.sleep(1)

    workdays()

except Exception as e:
    process_registrant.register_error('Exception from main module: '+str(e))
    process_registrant.call_critical()