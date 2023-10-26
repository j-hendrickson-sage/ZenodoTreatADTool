library(DT)
library(shiny)
library(reticulate)

if (!file.exists("python3_env")) utils::unzip("python3_env.zip")

reticulate::virtualenv_create(envname = 'python3_env')
reticulate::virtualenv_install('python3_env', packages = c('requests', "pandas"))
reticulate::use_virtualenv('python3_env', required = T)
reticulate::source_python("requestData.py")

ui <- basicPage(
  h2("The TREAT-AD Community Data"),
  DT::dataTableOutput("mytable"),
  fluidPage(theme = shinytheme("slate"),
    actionButton("action", label = "Pull Zenodo Data"),
    uiOutput("downloadData")
  )
)

server <- function(input, output) {
  
  df <- reactive({
    response_treatad <- getResponse(community = "treatad")
    response_ycharos <- getResponse(community = "ycharos")
    rbind(requestData(response = response_treatad, communityDisplayName = "TREAT-AD"),requestData(response = response_ycharos, communityDisplayName = "YCharOS")) 
  }) %>%
    bindEvent(input$action)
  
  output$mytable = DT::renderDataTable({
    df()
  })
  
  output$downloadData <- renderUI({
    req(input$action, df())
    downloadButton("downloadData01")
  })
  
  output$downloadData01 <- downloadHandler(
    filename = function() {
      paste0(Sys.Date(), "_TREATAD_Zenodo.csv")
    },
    content = function(fname) {
      write.csv(df(), fname)
    }
  )
}

shinyApp(ui, server)